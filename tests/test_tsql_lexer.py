import unittest
import pytest
from tsql_lexer import lex, EnumTokenType, EnumValueId

vpit="""
use liga;
drop view if exists vpit;
create VIEW vpit as
with 
 resultados_acumulado as(	select distinct temporada, division, jornada
							, elocal
							, glocal
							, sum(1) over (partition by temporada, division, elocal order by jornada) as JC
							, sum(glocal) over (partition by temporada, division, elocal order by jornada) as GFC
							, sum(gvisitante) over (partition by temporada, division, elocal order by jornada) as GCC
							, sum(case when glocal > gvisitante then 1 else 0 end) over (partition by temporada, division, elocal order by jornada) as GC
							, sum(case when glocal = gvisitante then 1 else 0 end) over (partition by temporada, division, elocal order by jornada) as EC
							, sum(case when glocal < gvisitante then 1 else 0 end) over (partition by temporada, division, elocal order by jornada) as PC
							, evisitante
							, gvisitante
							, sum(1) over (partition by temporada, division, evisitante order by jornada) as JF
							, sum(gvisitante) over (partition by temporada, division, evisitante order by jornada) as GFF
							, sum(glocal) over (partition by temporada, division, evisitante order by jornada) as GCF
							, sum(case when glocal < gvisitante then 1 else 0 end) over (partition by temporada, division, evisitante order by jornada) as GF
							, sum(case when glocal = gvisitante then 1 else 0 end) over (partition by temporada, division, evisitante order by jornada) as EF
							, sum(case when glocal > gvisitante then 1 else 0 end) over (partition by temporada, division, evisitante order by jornada) as PF
							, (glocal+1)/(cast(gvisitante+1 as decimal)) as ratio_glocal_1
							, (gvisitante+1)/(cast(glocal+1 as decimal)) as ratio_gvisitante_1
							from resultados as r 
						)
							
,promedios as			(	select*
							, GFC /cast(JC as decimal) as prom_gfc
							, GCC /cast(JC as decimal) as prom_gcc
							, GC /cast(JC as decimal) as prom_gc
							, EC /cast(JC as decimal) as prom_ec
							, PC /cast(JC as decimal) as prom_pc

							, GFF / cast(JF as decimal) as prom_gff
							, GCF / cast(JF as decimal) as prom_gcf
							, GF / cast(JF as decimal) as prom_gf
							, EF / cast(JF as decimal) as prom_ef
							, PF / cast(JF as decimal) as prom_pf

							from resultados_acumulado as r
							where glocal is not null and gvisitante is not null
						)
select 
  row_number()over(partition by r.division, r.temporada order by r.jornada desc, r.elocal) as rn
, r.*
, l.prom_gfc as A
, l.prom_gcc as B
, l.prom_gc as C
, l.prom_ec as D
, l.prom_pc as E
, v.prom_gff as F
, v.prom_gcf as G
, v.prom_gf as H
, v.prom_ef as I
, v.prom_pf as J
, dense_rank() over(partition by r.division, r.temporada order by r.jornada desc) as K
FROM resultados_acumulado as r
left join promedios l on l.temporada = r.temporada and l.division = r.division and l.elocal = r.elocal and l.glocal is not null
		and l.jc = (select max(jc)
					from promedios u 
					where u.temporada = r.temporada 
					and u.division = r.division 
					and u.elocal = r.elocal 
					and u.jc <= r.jc - 1
					) #r.jc -1
left join promedios v on v.temporada = r.temporada and v.division = r.division and v.evisitante = r.evisitante and v.glocal is not null
		and v.jf = (select max(jf)
					from promedios u 
					where u.temporada = r.temporada 
					and u.division = r.division 
					and u.evisitante = r.evisitante
					and u.jf <= r.jf - 1
					) #r.jf -1
order by r.division desc, r.temporada desc, r.jornada desc, r.elocal
"""

@pytest.fixture
def lexed_tokens(): return lambda query: [tok for tok in lex(query)]

@pytest.mark.parametrize("sql, expected",[
    # Keywords
    ("left", ["LEFT"]),
    ("left join", ["LEFT JOIN"]),
    ("hello left join", ["HELLO", "LEFT JOIN"]),
    ("left outer", ["LEFT", "OUTER"]),
    ("left outer join", ["LEFT OUTER JOIN"]),
    ("left . join", ["LEFT", ".", "JOIN"]),
    ("left = join", ["LEFT", "=", "JOIN"]),
    ("left join t", ["LEFT JOIN", "T"]),
    ("left join t left join", ["LEFT JOIN", "T", "LEFT JOIN"]),
    # Identifiers
    ("serv", ["SERV"]),
    ("serv.", ["SERV", "."]),
    ("serv.db", ["SERV.DB"]),
    ("serv.db.", ["SERV.DB", "."]),
    ("serv.db.dbo", ["SERV.DB.DBO"]),
    ("serv.db.dbo.", ["SERV.DB.DBO", "."]),
    ("serv.db.dbo.table1", ["SERV.DB.DBO.TABLE1"]),
    ("serv.db.dbo.table1.", ["SERV.DB.DBO.TABLE1", "."]),
    ("serv.db.dbo.table1..", ["SERV.DB.DBO.TABLE1.."]),
    ("serv.db.dbo.table1>.", ["SERV.DB.DBO.TABLE1", ">", "."]),
    ('[serv]."db".[dbo]."table1"', ['[serv]."db".[dbo]."table1"']),
    # Keyword precedence
    ("serv.db.dbo.join", ["SERV.DB.DBO", ".", "JOIN"]),
    ("serv.db.dbo.join.", ["SERV.DB.DBO", ".", "JOIN", "."]),
    ("serv.db.dbo.left.join.", ["SERV.DB.DBO", ".", "LEFT", ".", "JOIN", "."]),
    ("serv.db.dbo.left join.", ["SERV.DB.DBO", ".", "LEFT JOIN", "."]),
    ("serv.db.dbo.right join.", ["SERV.DB.DBO", ".", "RIGHT JOIN", "."]),
    ("serv.db.dbo.right outer join.", ["SERV.DB.DBO", ".", "RIGHT OUTER JOIN", "."]),
    ("tabla.within group", ["TABLA", ".", "WITHIN GROUP"]),
    #flush buffer
    ("left outer join left outer join", ["LEFT OUTER JOIN", "LEFT OUTER JOIN"]),
    ("left join t.a left join", ["LEFT JOIN", "T.A", "LEFT JOIN"]),
])
def test_tsql_lexer_keywords(sql, expected): assert [t.value for t in lex(sql)] == [t for t in expected]


def test_end():
    tokens  = [tok for tok in lex("from   a left  outer   join b cross join c")]
    assert tokens[1].end == 8
    assert tokens[2].end == 27
    assert tokens[4].end == 40

def test_keyword_identifier():
    tokens  = [tok for tok in lex("select a where 1 = 1")]
    assert tokens[0].type == EnumTokenType.KEYWORD
    assert tokens[1].type == EnumTokenType.IDENTIFIER
    assert tokens[2].type == EnumTokenType.KEYWORD
    assert tokens[4].type not in [EnumTokenType.KEYWORD, EnumTokenType.IDENTIFIER]

@pytest.mark.parametrize("sql, expected",[
    ("select*from table1", [EnumValueId.SELECT, EnumValueId.OP_MUL, EnumValueId.FROM, None]), 
    ("+-*/%", [EnumValueId.OP_ADD, EnumValueId.OP_SUB, EnumValueId.OP_MUL, EnumValueId.OP_DIV, EnumValueId.OP_MOD]), 
])
def test_value_id(sql, expected): assert [t.value_id for t in lex(sql)] == expected

def test_has_value_id():
    tokens = [tok for tok in lex(vpit)]
    for t in tokens:
        if t.type not in (EnumTokenType.IDENTIFIER, EnumTokenType.INTEGER, EnumTokenType.DECIMAL):
        	assert t.value_id != None