import unittest
import re
from tokenizer import Token, tokenize

class TokenizerTest(unittest.TestCase):
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

	def test_numbers(self):
		sql = '12.123.456e+489.12esdf'
		self.assertEqual([('12.123', True), ('.456e+489', True),('.12e', True), ('sdf', False)], [(t.get_value(sql), (t.type==2)) for t in tokenize(sql)] )

	def test_is_number(self):
		self.assertNotIn(True, [(t.type==2) for t in tokenize("as campo .ae-a -taba")] )
		self.assertEqual([True, True, False, True, True], [(t.type==2) for t in tokenize("2 12.23e-49 a7.8 7.8")] )
		self.assertEqual([True, True], [(t.type==2) for t in tokenize("12.23e-49 .8")] )

	def test_no_blanks(self):
		sql = """ SELECT

		*		  from  
		    
		"""
		self.assertEqual(['SELECT', '*','from'], [(t.get_value(sql)) for t in tokenize(sql)] )

	def test_comments(self):
		sql = """select --line comment
		*/*
		block comment
		*/from 
		"""
		toks = [t for t in tokenize(sql)]
		self.assertEqual(['select', '*','from'], [(t.get_value(sql)) for t in toks if t.type not in[6,7]] )
		self.assertEqual(toks[1].get_value(sql,), '--line comment\n')
		self.assertEqual(toks[3].get_value(sql,), """/*
		block comment
		*/""")

		sql = """Nested/*this's a line comment
		simple-- this/*, another 
		one*/
		example */blockcomment
		"""
		toks = [t for t in tokenize(sql)]
		self.assertEqual(toks[1].get_value(sql),"""/*this's a line comment
		simple-- this/*, another 
		one*/
		example */""")
	
	def test_delimited_construct_0(self):
		sql = "'u'a"
		self.assertEqual([("'u'", True), ("a", False)], [(t.get_value(sql), (t.type==3)) for t in tokenize(sql)] )

	def test_delimited_construct_1(self):
		sql = "'uno''dos''tres'"
		self.assertEqual([("'uno''dos''tres'", True)], [(t.get_value(sql), (t.type==3)) for t in tokenize(sql)] )
		sql = "'uno''dos' 'tres'"
		self.assertEqual([("'uno''dos'", True), ("'tres'", True)], [(t.get_value(sql), (t.type==3)) for t in tokenize(sql)] )

	def test_delimited_construct_2(self):
		sql = """['uno']]dos]' [
'']'tres"""
		self.assertEqual([("['uno']]dos]", True), ("' [\n'']'", True), ("tres", False)], [(t.get_value(sql), (t.type==3)) for t in tokenize(sql)] )

	def test_types(self):
		sql = "identi 12.3e-45 [delimited literal] >= < ,"
		self.assertEqual([1,2,3,4,4,5], [t.type for t in tokenize(sql)] )
		sql = "/*block comment*/ --line comment"
		self.assertEqual([7,6], [t.type for t in tokenize(sql)] )

	def test_code_integrity(self):
		normalized = self.vpit.strip().upper()
		normalized = re.sub(r'([;(),\+\-\*\/.])', r' \1 ', normalized)
		normalized = re.sub(r'\s+', ' ', normalized)

		uppered = self.vpit.upper()
		tokenized = " ".join([t.get_value(uppered) for t in tokenize(uppered)])
		self.assertEqual(normalized, tokenized)
	def test_delimiters(self):
		sql = "1,"
		values = [tok.get_value(sql=sql) for tok in tokenize(sql)]
		self.assertEqual(["1",","], values)
		sql = "(1,'2025-09-06', 2.56e41, 7)"
		values = [(tok.get_value(sql=sql), tok.type == 2) for tok in tokenize(sql)]
		self.assertEqual([("(", False),("1", True), (",", False), ("'2025-09-06'", False), (",", False), ("2.56e41", True), (",", False), ("7", True), (")", False)], values)

class CurrentTest(unittest.TestCase):
	pass


if __name__ == '__main__':
	unittest.main()