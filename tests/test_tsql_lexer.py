import unittest
import pytest
from tsql_lexer import lex, EnumTokenSubtype, EnumTokenType

@pytest.fixture
def lexed_tokens(): return lambda query: [tok for tok in lex(query)]

@pytest.mark.parametrize("sql, expected",[
    # Keywords
    ("left", ["LEFT"]),
    ("left join", ["LEFT JOIN"]),
    ("hello left join", ["hello", "LEFT JOIN"]),
    ("left outer", ["LEFT", "OUTER"]),
    ("left outer join", ["LEFT OUTER JOIN"]),
    ("left . join", ["LEFT", ".", "JOIN"]),
    ("left = join", ["LEFT", "=", "JOIN"]),
    ("left join t", ["LEFT JOIN", "t"]),
    ("left join t left join", ["LEFT JOIN", "t", "LEFT JOIN"]),
    # Identifiers
    ("serv", ["serv"]),
    ("serv.", ["serv", "."]),
    ("serv.db", ["serv.db"]),
    ("serv.db.", ["serv.db", "."]),
    ("serv.db.dbo", ["serv.db.dbo"]),
    ("serv.db.dbo.", ["serv.db.dbo", "."]),
    ("serv.db.dbo.table1", ["serv.db.dbo.table1"]),
    ("serv.db.dbo.table1.", ["serv.db.dbo.table1", "."]),
    ("serv.db.dbo.table1..", ["serv.db.dbo.table1.."]),
    ("serv.db.dbo.table1>.", ["serv.db.dbo.table1", ">", "."]),
    ('[serv]."db".[dbo]."table1"', ['[serv]."db".[dbo]."table1"']),
    # Keyword precedence
    ("serv.db.dbo.join", ["serv.db.dbo", ".", "JOIN"]),
    ("serv.db.dbo.join.", ["serv.db.dbo", ".", "JOIN", "."]),
    ("serv.db.dbo.left.join.", ["serv.db.dbo", ".", "LEFT", ".", "JOIN", "."]),
    ("serv.db.dbo.left join.", ["serv.db.dbo", ".", "LEFT JOIN", "."]),
    ("tabla.within group", ["tabla", ".", "WITHIN GROUP"]),
    #flush buffer
    ("left outer join left outer join", ["LEFT OUTER JOIN", "LEFT OUTER JOIN"]),
    ("left join t.a left join", ["LEFT JOIN", "t.a", "LEFT JOIN"]),
])
def test_tsql_lexer_keywords(sql, expected): assert [t.value for t in lex(sql)] == expected


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

def test_keyword_subtype():
    tokens  = [tok for tok in lex("left outer join #b group by case @var=field")]
    assert tokens[0].subtype == EnumTokenSubtype.RELATIONAL_OPERATORS
    assert tokens[1].subtype == EnumTokenSubtype.TEMPORARY_OBJECT
    assert tokens[2].subtype == EnumTokenSubtype.QUERY_CLAUSES
    assert tokens[3].subtype == EnumTokenSubtype.FLOW_CONTROL
    assert tokens[4].subtype == EnumTokenSubtype.VARIABLE

def test_is_starter_keyword():
    tokens  = [tok for tok in lex("join b select set")]
    assert tokens[0].is_starter_keyword == False
    assert tokens[2].is_starter_keyword == True
    assert tokens[3].is_starter_keyword == True
