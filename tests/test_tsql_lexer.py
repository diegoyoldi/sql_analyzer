import unittest
from tsql_lexer import lex, TokenSubtype

class TestTsqlLexser(unittest.TestCase):

    def test_lex_keywords(self):
        self.assertEqual([t.value for t in lex("left")], ["LEFT"])
        self.assertEqual([t.value for t in lex("left join")], ["LEFT JOIN"])
        self.assertEqual([t.value for t in lex("hello left join")], ["hello", "LEFT JOIN"])
        self.assertEqual([t.value for t in lex("left outer")], ["LEFT", "OUTER"])
        self.assertEqual([t.value for t in lex("left outer join")], ["LEFT OUTER JOIN"])
        self.assertEqual([t.value for t in lex("left . join")], ["LEFT", ".", "JOIN"])
        self.assertEqual([t.value for t in lex("left = join")], ["LEFT", "=", "JOIN"])
        self.assertEqual([t.value for t in lex("left join t")], ["LEFT JOIN", "t"])
        self.assertEqual([t.value for t in lex("left join t left join")], ["LEFT JOIN", "t", "LEFT JOIN"])

    def test_lex_identifiers(self):
        self.assertEqual([t.value for t in lex("serv")], ["serv"])
        self.assertEqual([t.value for t in lex("serv.")], ["serv", "."])
        self.assertEqual([t.value for t in lex("serv.db")], ["serv.db"])
        self.assertEqual([t.value for t in lex("serv.db.")], ["serv.db", "."])
        self.assertEqual([t.value for t in lex("serv.db.dbo")], ["serv.db.dbo"])
        self.assertEqual([t.value for t in lex("serv.db.dbo.")], ["serv.db.dbo", "."])
        self.assertEqual([t.value for t in lex("serv.db.dbo.table1")], ["serv.db.dbo.table1"])
        self.assertEqual([t.value for t in lex("serv.db.dbo.table1.")], ["serv.db.dbo.table1", "."])
        self.assertEqual([t.value for t in lex("serv.db.dbo.table1..")], ["serv.db.dbo.table1.."])
        self.assertEqual([t.value for t in lex("serv.db.dbo.table1>.")], ["serv.db.dbo.table1", ">", "."])

    def test_keyword_precedence(self):
        self.assertEqual([t.value for t in lex("serv.db.dbo.join")], ["serv.db.dbo", ".", "JOIN"])
        self.assertEqual([t.value for t in lex("serv.db.dbo.join.")], ["serv.db.dbo", ".", "JOIN", "."])
        self.assertEqual([t.value for t in lex("serv.db.dbo.left.join.")], ["serv.db.dbo", ".", "LEFT", ".", "JOIN", "."])
        self.assertEqual([t.value for t in lex("serv.db.dbo.left join.")], ["serv.db.dbo", ".", "LEFT JOIN", "."])
        self.assertEqual([t.value for t in lex("tabla.within group")], ["tabla", ".", "WITHIN GROUP"])

    def test_flush_buffer(self):
        self.assertEqual([t.value for t in lex("left outer join left outer join")], ["LEFT OUTER JOIN", "LEFT OUTER JOIN"])
        self.assertEqual([t.value for t in lex("left join t.a left join")], ["LEFT JOIN", "t.a", "LEFT JOIN"])

    def test_end(self):
        tokens  = [tok for tok in lex("from   a left  outer   join b cross join c")]
        self.assertEqual(tokens[1].end, 8)
        self.assertEqual(tokens[2].end, 27)
        self.assertEqual(tokens[4].end, 40)

    def test_keyword_identifier(self):
        tokens  = [tok for tok in lex("select a where 1 = 1")]
        self.assertEqual(tokens[0].type, 6)
        self.assertEqual(tokens[1].type, 7)
        self.assertEqual(tokens[2].type, 6)
        self.assertNotIn(tokens[4].type, [6, 7])

    def test_keyword_subtype(self):
        tokens  = [tok for tok in lex("left outer join #b group by case @var=field")]
        self.assertEqual(tokens[0].subtype.value, TokenSubtype.RELATIONAL_OPERATORS.value)
        self.assertEqual(tokens[1].subtype.value, TokenSubtype.TEMPORARY_OBJECT.value)
        self.assertEqual(tokens[2].subtype.value, TokenSubtype.QUERY_CLAUSES.value)
        self.assertEqual(tokens[3].subtype.value, TokenSubtype.FLOW_CONTROL.value)
        self.assertEqual(tokens[4].subtype.value, TokenSubtype.VARIABLE.value)
        self.assertFalse(hasattr(tokens[5], "subtype"))
        self.assertFalse(hasattr(tokens[6], "subtype"))

    def test_is_starter_keyword(self):
        tokens  = [tok for tok in lex("join b select set")]
        self.assertFalse(tokens[0].is_starter_keyword)
        self.assertFalse(hasattr(tokens[1], "is_starter_keyword"))
        self.assertTrue(tokens[2].is_starter_keyword)
        self.assertTrue(tokens[3].is_starter_keyword)

if __name__ == '__main__':
    unittest.main()    
