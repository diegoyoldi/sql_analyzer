import string
from typing import Iterator, Dict, List
import tokenizer
from enum import IntEnum

class TokenType(IntEnum):
	UNKNOWN = 0
	WORD = 1
	NUMBER = 2
	DELIMITED_LITERAL = 3
	OPERATOR = 4
	DELIMITER = 5	
	KEYWORD = 6
	IDENTIFIER = 7
	
class TokenSubtype(IntEnum):
	UNKNOWN = 0
	QUERY_CLAUSES = 1
	SET_OPERATORS = 2
	RELATIONAL_OPERATORS = 3
	SET_PREDICATE_OPERATORS = 4
	DDL = 5
	DML = 6
	TCL = 7
	DCL = 8
	FLOW_CONTROL = 9
	OTHER_KEYWORDS = 10
	VARIABLE = 11
	TEMPORARY_OBJECT = 12
	
class TSqlToken(tokenizer.Token):
	# __slots__ = ('value', 'subtype', 'is_starter_keyword')
	value:str
	subtype:int
	is_starter_keyword:bool

	def __init__(self, token:tokenizer.Token):
		self.start = token.start
		self.end = token.end
		self.type = token.type
		self.value:str = None
		# self.subtype:int = None
		# self.is_starter_keyword:bool = None

KEYWORDS = frozenset({
	'ADD', 'EXTERNAL', 'PROCEDURE', 'ALL', 'FETCH', 'PUBLIC', 'ALTER'
	, 'FILE', 'RAISERROR', 'AND', 'FILLFACTOR', 'READ', 'ANY', 'FOR'
	, 'READTEXT', 'AS', 'FOREIGN', 'RECONFIGURE', 'ASC', 'FREETEXT'
	, 'REFERENCES', 'AUTHORIZATION', 'FREETEXTTABLE', 'REPLICATION'
	, 'BACKUP', 'FROM', 'RESTORE', 'BEGIN', 'FULL', 'RESTRICT', 'BETWEEN'
	, 'FUNCTION', 'RETURN', 'BREAK', 'GOTO', 'REVERT', 'BROWSE', 'GRANT'
	, 'REVOKE', 'BULK', 'GROUP', 'RIGHT', 'BY', 'HAVING', 'ROLLBACK'
	, 'CASCADE', 'HOLDLOCK', 'ROWCOUNT', 'CASE', 'IDENTITY', 'ROWGUIDCOL'
	, 'CHECK', 'IDENTITY_INSERT', 'RULE', 'CHECKPOINT', 'IDENTITYCOL'
	, 'SAVE', 'CLOSE', 'IF', 'SCHEMA', 'CLUSTERED', 'IN', 'SECURITYAUDIT'
	, 'COALESCE', 'INDEX', 'SELECT', 'COLLATE', 'INNER', 'SEMANTICKEYPHRASETABLE'
	, 'COLUMN', 'INSERT', 'SEMANTICSIMILARITYDETAILSTABLE', 'COMMIT', 'INTERSECT'
	, 'SEMANTICSIMILARITYTABLE', 'COMPUTE', 'INTO', 'SESSION_USER', 'CONSTRAINT'
	, 'IS', 'SET', 'CONTAINS', 'JOIN', 'SETUSER', 'CONTAINSTABLE', 'KEY'
	, 'SHUTDOWN', 'CONTINUE', 'KILL', 'SOME', 'CONVERT', 'LEFT', 'STATISTICS'
	, 'CREATE', 'LIKE', 'SYSTEM_USER', 'CROSS', 'LINENO', 'TABLE', 'CURRENT'
	, 'LOAD', 'TABLESAMPLE', 'CURRENT_DATE', 'MERGE', 'TEXTSIZE'
	, 'CURRENT_TIME', 'NATIONAL', 'THEN', 'CURRENT_TIMESTAMP', 'NOCHECK'
	, 'TO', 'CURRENT_USER', 'NONCLUSTERED', 'TOP', 'CURSOR'
	, 'NOT', 'TRAN', 'DATABASE', 'NULL', 'TRANSACTION', 'DBCC', 'NULLIF'
	, 'TRIGGER', 'DEALLOCATE', 'OF', 'TRUNCATE', 'DECLARE', 'OFF'
	, 'TRY_CONVERT', 'DEFAULT', 'OFFSETS', 'TSEQUAL', 'DELETE', 'ON'
	, 'UNION', 'DENY', 'OPEN', 'UNIQUE', 'DESC', 'OPENDATASOURCE', 'UNPIVOT'
	, 'DISK', 'OPENQUERY', 'UPDATE', 'DISTINCT', 'OPENROWSET', 'UPDATETEXT'
	, 'DISTRIBUTED', 'OPENXML', 'USE', 'DOUBLE', 'OPTION', 'USER', 'DROP'
	, 'OR', 'VALUES', 'DUMP', 'ORDER', 'VARYING', 'ELSE', 'OUTER', 'VIEW'
	, 'END', 'OVER', 'WAITFOR', 'ERRLVL', 'PERCENT', 'WHEN', 'ESCAPE', 'PIVOT'
	, 'WHERE', 'EXCEPT', 'PLAN', 'WHILE', 'EXEC', 'PRECISION', 'WITH', 'EXECUTE'
	, 'PRIMARY'#, 'WITHIN GROUP'
	, 'EXISTS', 'PRINT', 'WRITETEXT', 'EXIT', 'PROC'
})

STARTER_KEYWORDS = frozenset({
	'SELECT', 'UPDATE', 'INSERT', 'DELETE', 'MERGE', 'CREATE', 'DROP', 'TRUNCATE', 'ALTER', 'EXEC', 'EXECUTE', 
	'DECLARE', 'SET', 'COMMIT', 'ROLLBACK', 'USE', 'GRANT', 'DENY', 'REVOKE', 'SAVE', 'BACKUP', 
	'RESTORE', 'PRINT', 'GOTO', 'RETURN', 'IF', 'WHILE'
})

_KEYWORD_SUBTYPES_1 = {'SESSION_USER': TokenSubtype.UNKNOWN, 'VIEW': TokenSubtype.UNKNOWN, 'NOT': TokenSubtype.UNKNOWN, 'TSEQUAL': TokenSubtype.UNKNOWN, 'SECURITYAUDIT': TokenSubtype.UNKNOWN, 'CONVERT': TokenSubtype.UNKNOWN, 'BROWSE': TokenSubtype.UNKNOWN, 'UNPIVOT': TokenSubtype.UNKNOWN, 'ROWCOUNT': TokenSubtype.UNKNOWN, 'RETURN': TokenSubtype.FLOW_CONTROL, 'SEMANTICSIMILARITYDETAILSTABLE': TokenSubtype.UNKNOWN, 'PROCEDURE': TokenSubtype.UNKNOWN, 'DENY': TokenSubtype.DCL, 'PIVOT': TokenSubtype.UNKNOWN, 'AND': TokenSubtype.UNKNOWN, 'TOP': TokenSubtype.QUERY_CLAUSES, 'INTO': TokenSubtype.UNKNOWN, 'SET': TokenSubtype.OTHER_KEYWORDS, 'END': TokenSubtype.UNKNOWN, 'CASE': TokenSubtype.FLOW_CONTROL, 'CHECK': TokenSubtype.UNKNOWN, 'COLUMN': TokenSubtype.UNKNOWN, 'EXECUTE': TokenSubtype.UNKNOWN, 'DISK': TokenSubtype.UNKNOWN, 'MERGE': TokenSubtype.DML, 'INNER': TokenSubtype.UNKNOWN, 'NATIONAL': TokenSubtype.UNKNOWN, 'ERRLVL': TokenSubtype.UNKNOWN, 'TEXTSIZE': TokenSubtype.UNKNOWN, 'DROP': TokenSubtype.DDL, 'USER': TokenSubtype.UNKNOWN, 'DBCC': TokenSubtype.UNKNOWN, 'AS': TokenSubtype.UNKNOWN, 'HAVING': TokenSubtype.QUERY_CLAUSES, 'BACKUP': TokenSubtype.UNKNOWN, 'WHEN': TokenSubtype.UNKNOWN, 'CURRENT_TIME': TokenSubtype.UNKNOWN, 'OPTION': TokenSubtype.OTHER_KEYWORDS, 'SHUTDOWN': TokenSubtype.UNKNOWN, 'CLOSE': TokenSubtype.UNKNOWN, 'IDENTITY': TokenSubtype.UNKNOWN, 'IS': TokenSubtype.UNKNOWN, 'NOCHECK': TokenSubtype.UNKNOWN, 'PRECISION': TokenSubtype.UNKNOWN, 'FOR': TokenSubtype.UNKNOWN, 'PUBLIC': TokenSubtype.UNKNOWN, 'OR': TokenSubtype.UNKNOWN, 'THEN': TokenSubtype.UNKNOWN, 'FREETEXT': TokenSubtype.UNKNOWN, 'CURSOR': TokenSubtype.UNKNOWN, 'REFERENCES': TokenSubtype.UNKNOWN, 'DECLARE': TokenSubtype.OTHER_KEYWORDS, 'CURRENT_DATE': TokenSubtype.UNKNOWN, 'FREETEXTTABLE': TokenSubtype.UNKNOWN, 'CROSS': TokenSubtype.UNKNOWN, 'TRIGGER': TokenSubtype.UNKNOWN, 'CURRENT': TokenSubtype.UNKNOWN, 'BETWEEN': TokenSubtype.UNKNOWN, 'LIKE': TokenSubtype.UNKNOWN, 'EXEC': TokenSubtype.OTHER_KEYWORDS, 'GOTO': TokenSubtype.FLOW_CONTROL, 'CONTINUE': TokenSubtype.FLOW_CONTROL, 'ESCAPE': TokenSubtype.UNKNOWN, 'NULLIF': TokenSubtype.UNKNOWN, 'NONCLUSTERED': TokenSubtype.UNKNOWN, 'FILE': TokenSubtype.UNKNOWN, 'ON': TokenSubtype.UNKNOWN, 'RECONFIGURE': TokenSubtype.UNKNOWN, 'COMMIT': TokenSubtype.TCL, 'COLLATE': TokenSubtype.UNKNOWN, 'OVER': TokenSubtype.UNKNOWN, 'SEMANTICSIMILARITYTABLE': TokenSubtype.UNKNOWN, 'FETCH': TokenSubtype.UNKNOWN, 'SEMANTICKEYPHRASETABLE': TokenSubtype.UNKNOWN, 'TABLESAMPLE': TokenSubtype.UNKNOWN, 'FILLFACTOR': TokenSubtype.UNKNOWN, 'DATABASE': TokenSubtype.UNKNOWN, 'DELETE': TokenSubtype.DML, 'OPENDATASOURCE': TokenSubtype.UNKNOWN, 'RESTORE': TokenSubtype.UNKNOWN, 'IDENTITY_INSERT': TokenSubtype.UNKNOWN, 'KILL': TokenSubtype.UNKNOWN, 'INTERSECT': TokenSubtype.SET_OPERATORS, 'GRANT': TokenSubtype.DCL, 'CONTAINSTABLE': TokenSubtype.UNKNOWN, 'FROM': TokenSubtype.QUERY_CLAUSES, 'VALUES': TokenSubtype.UNKNOWN, 'TRY_CONVERT': TokenSubtype.UNKNOWN, 'EXIT': TokenSubtype.UNKNOWN, 'DOUBLE': TokenSubtype.UNKNOWN, 'CURRENT_TIMESTAMP': TokenSubtype.UNKNOWN, 'PROC': TokenSubtype.UNKNOWN, 'EXCEPT': TokenSubtype.SET_OPERATORS, 'HOLDLOCK': TokenSubtype.UNKNOWN, 'WHERE': TokenSubtype.QUERY_CLAUSES, 'PLAN': TokenSubtype.UNKNOWN, 'TABLE': TokenSubtype.UNKNOWN, 'CONTAINS': TokenSubtype.UNKNOWN, 'REVOKE': TokenSubtype.DCL, 'REPLICATION': TokenSubtype.UNKNOWN, 'ASC': TokenSubtype.UNKNOWN, 'TRUNCATE': TokenSubtype.DDL, 'IN': TokenSubtype.SET_PREDICATE_OPERATORS, 'ADD': TokenSubtype.UNKNOWN, 'READTEXT': TokenSubtype.UNKNOWN, 'REVERT': TokenSubtype.UNKNOWN, 'COALESCE': TokenSubtype.UNKNOWN, 'USE': TokenSubtype.OTHER_KEYWORDS, 'CURRENT_USER': TokenSubtype.UNKNOWN, 'OPENQUERY': TokenSubtype.UNKNOWN, 'LOAD': TokenSubtype.UNKNOWN, 'OF': TokenSubtype.UNKNOWN, 'DUMP': TokenSubtype.UNKNOWN, 'LINENO': TokenSubtype.UNKNOWN, 'EXISTS': TokenSubtype.SET_PREDICATE_OPERATORS, 'OFF': TokenSubtype.UNKNOWN, 'UNION': TokenSubtype.SET_OPERATORS, 'DISTRIBUTED': TokenSubtype.UNKNOWN, 'VARYING': TokenSubtype.UNKNOWN, 'DESC': TokenSubtype.UNKNOWN, 'SYSTEM_USER': TokenSubtype.UNKNOWN, 'IF': TokenSubtype.FLOW_CONTROL, 'ELSE': TokenSubtype.FLOW_CONTROL, 'OPENXML': TokenSubtype.UNKNOWN, 'SETUSER': TokenSubtype.UNKNOWN, 'CLUSTERED': TokenSubtype.UNKNOWN, 'WHILE': TokenSubtype.FLOW_CONTROL, 'WITH': TokenSubtype.OTHER_KEYWORDS, 'LEFT': TokenSubtype.UNKNOWN, 'ROLLBACK': TokenSubtype.TCL, 'WAITFOR': TokenSubtype.UNKNOWN, 'SCHEMA': TokenSubtype.UNKNOWN, 'DISTINCT': TokenSubtype.UNKNOWN, 'BULK': TokenSubtype.UNKNOWN, 'FUNCTION': TokenSubtype.UNKNOWN, 'SAVE': TokenSubtype.UNKNOWN, 'CONSTRAINT': TokenSubtype.UNKNOWN, 'UPDATETEXT': TokenSubtype.UNKNOWN, 'CASCADE': TokenSubtype.UNKNOWN, 'FOREIGN': TokenSubtype.UNKNOWN, 'OPEN': TokenSubtype.UNKNOWN, 'ALL': TokenSubtype.SET_PREDICATE_OPERATORS, 'BREAK': TokenSubtype.FLOW_CONTROL, 'ROWGUIDCOL': TokenSubtype.UNKNOWN, 'TRANSACTION': TokenSubtype.UNKNOWN, 'UPDATE': TokenSubtype.DML, 'ANY': TokenSubtype.SET_PREDICATE_OPERATORS, 'BY': TokenSubtype.UNKNOWN, 'ORDER': TokenSubtype.UNKNOWN, 'EXTERNAL': TokenSubtype.UNKNOWN, 'KEY': TokenSubtype.UNKNOWN, 'TRAN': TokenSubtype.UNKNOWN, 'OFFSETS': TokenSubtype.UNKNOWN, 'RAISERROR': TokenSubtype.UNKNOWN, 'SELECT': TokenSubtype.QUERY_CLAUSES, 'CREATE': TokenSubtype.DDL, 'GROUP': TokenSubtype.UNKNOWN, 'FULL': TokenSubtype.UNKNOWN, 'ALTER': TokenSubtype.DDL, 'READ': TokenSubtype.UNKNOWN, 'INSERT': TokenSubtype.DML, 'BEGIN': TokenSubtype.UNKNOWN, 'STATISTICS': TokenSubtype.UNKNOWN, 'OUTER': TokenSubtype.UNKNOWN, 'OPENROWSET': TokenSubtype.UNKNOWN, 'SOME': TokenSubtype.SET_PREDICATE_OPERATORS, 'RULE': TokenSubtype.UNKNOWN, 'AUTHORIZATION': TokenSubtype.UNKNOWN, 'PRINT': TokenSubtype.OTHER_KEYWORDS, 'DEALLOCATE': TokenSubtype.UNKNOWN, 'PERCENT': TokenSubtype.UNKNOWN, 'RIGHT': TokenSubtype.UNKNOWN, 'INDEX': TokenSubtype.UNKNOWN, 'JOIN': TokenSubtype.RELATIONAL_OPERATORS, 'PRIMARY': TokenSubtype.UNKNOWN, 'UNIQUE': TokenSubtype.UNKNOWN, 'WRITETEXT': TokenSubtype.UNKNOWN, 'COMPUTE': TokenSubtype.UNKNOWN, 'RESTRICT': TokenSubtype.UNKNOWN, 'TO': TokenSubtype.UNKNOWN, 'DEFAULT': TokenSubtype.UNKNOWN, 'NULL': TokenSubtype.UNKNOWN, 'CHECKPOINT': TokenSubtype.UNKNOWN, 'IDENTITYCOL': TokenSubtype.UNKNOWN}
_KEYWORD_SUBTYPES_2 = {('INNER', 'JOIN'): ['INNER JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('CROSS', 'JOIN'): ['CROSS JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('COMMIT', 'TRAN'): ['COMMIT TRAN', None], ('ADD', 'CONSTRAINT'): ['ADD CONSTRAINT', None], ('WITHIN', 'GROUP'): ['WITHIN GROUP', None], ('BEGIN', 'TRAN'): ['BEGIN TRAN', None], ('CROSS', 'APPLY'): ['CROSS APPLY', None], ('BEGIN', 'TRANSACTION'): ['BEGIN TRANSACTION', TokenSubtype.TCL], ('ROLLBACK', 'TRANSACTION'): ['ROLLBACK TRANSACTION', None], ('BEGIN', 'TRY'): ['BEGIN TRY', None], ('GROUP', 'BY'): ['GROUP BY', TokenSubtype.QUERY_CLAUSES], ('END', 'CATCH'): ['END CATCH', None], ('FULL', 'JOIN'): ['FULL JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('COMMIT', 'TRANSACTION'): ['COMMIT TRANSACTION', None], ('ADD', 'COLUMN'): ['ADD COLUMN', None], ('BEGIN', 'CATCH'): ['BEGIN CATCH', None], ('LEFT', 'JOIN'): ['LEFT JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('ROLLBACK', 'TRAN'): ['ROLLBACK TRAN', None], ('ORDER', 'BY'): ['ORDER BY', TokenSubtype.QUERY_CLAUSES], ('END', 'TRY'): ['END TRY', None], ('RIGHT', 'JOIN'): ['RIGHT JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('OUTER', 'APPLY'): ['OUTER APPLY', None], ('IS', 'NULL'): ['IS NULL', None]}
_KEYWORD_SUBTYPES_3 = {('RIGHT', 'OUTER', 'JOIN'): ['RIGHT OUTER JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('LEFT', 'OUTER', 'JOIN'): ['LEFT OUTER JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('FULL', 'OUTER', 'JOIN'): ['FULL OUTER JOIN', TokenSubtype.RELATIONAL_OPERATORS], ('IS', 'NOT', 'NULL'): ['IS NOT NULL', None]}

def split_batches(sql: str, batch_separator: str = 'GO') -> List[str]:
	"""
	Split a SQL script into batches separated by a delimiter (default 'GO').

	Args:
		sql (str): Full SQL script to be split.
		batch_separator (str, optional): String that marks the batch separator. 
			Leading/trailing spaces and case are ignored. 
			Default is 'GO'.

	Returns:
		List[str]: List of SQL batches without the separator.
	"""
	batches, current = [], []
	append_batch = batches.append
	join = '\n'.join
	normalize = str.casefold
	batch_separator = normalize(batch_separator.strip())

	for line in sql.split("\n"):
		if normalize(line.strip()) == batch_separator:
			if current:
				batch = join(current).strip()
				if batch:
					append_batch(batch)
				current.clear()
		else:
			current.append(line)

	if current:
		batch = join(current).strip()
		if batch:
			append_batch(batch)

	return batches

def find_token_at(self, tokens: List[TSqlToken], position: int) -> TSqlToken | None:
	"""
	Find the token that covers a given character position.

	Args:
		tokens (List[TSqlToken]): List of tokens to search.
		position (int): Character index within the SQL script.

	Returns:
		TSqlToken | None: The token that contains the position, or None if not found.
	"""	
	return next((t for t in tokens if t.start <= position < t.end), None)

def _flush_buffer(buf: list[TSqlToken]) -> Iterator[TSqlToken]:

	# Compound Keywords
	i=0
	while i < len(buf):
		pending = len(buf) - i
		if pending >=3 and (subtype := _KEYWORD_SUBTYPES_3.get((buf[i].value.upper(), buf[i+1].value.upper(), buf[i+2].value.upper()))) != None:
			buf[i].value = subtype[0]
			buf[i].end = buf[i+2].end
			buf[i].type = TokenType.KEYWORD.value
			buf[i].subtype = subtype[1]
			del buf[i+1:i+3]
		elif pending >= 2 and (subtype := _KEYWORD_SUBTYPES_2.get((buf[i].value.upper(), buf[i+1].value.upper()))) != None:
			buf[i].value = subtype[0]
			buf[i].end = buf[i+1].end
			buf[i].type = TokenType.KEYWORD.value
			buf[i].subtype = subtype[1]
			del buf[i+1:i+2]
		elif (subtype := _KEYWORD_SUBTYPES_1.get(buf[i].value.upper())) != None:
			buf[i].value = buf[i].value.upper()
			buf[i].type = TokenType.KEYWORD.value
			buf[i].subtype = subtype
			buf[i].is_starter_keyword = buf[i].value in STARTER_KEYWORDS
		i += 1

	while buf:
		# Merge dotted identifiers
		if buf[0].type == TokenType.WORD.value:
			buf[0].type = TokenType.IDENTIFIER.value
			c = buf[0].value[0]
			if c == '@': buf[0].subtype = TokenSubtype.VARIABLE
			elif c == '#': buf[0].subtype = TokenSubtype.TEMPORARY_OBJECT
			while len(buf) >= 3 and buf[1].value == '.' and buf[2].type != TokenType.KEYWORD.value:
				buf[0].value += '.' + buf[2].value
				buf[0].end = buf[2].end
				del buf[1:3]

		yield buf.pop(0)

def lex(sql) -> Iterator[TSqlToken]:
	"""
	Lexical analyzer for SQL code. Splits a SQL script into tokens.

	Args:
		sql (str): The SQL script to tokenize.

	Yields:
		TSqlToken: Tokens extracted from the SQL script, including words,
		operators, comments, and delimiters.

	Notes:
		- Handles SQL-specific constructs such as:
			* Word starts: `_`, `@`, `#`, and letters.
			* Word characters: `_`, `@`, `#`, `$`, letters, digits.
			* Delimited identifiers and strings: `'...'`, `"..."`, `[...]`.
			* Line comments: `--`.
			* Block comments: `/* ... */`.
			* Operators (single-char and two-char).
		- Buffers consecutive words and dots (`.`) before yielding.
	"""
	it = tokenizer.tokenize(text=sql,
				word_start=frozenset('_@#' + string.ascii_letters),
				word_chars=frozenset('_@#$' + string.ascii_letters + string.digits),
				delimited_constructs={"'": "'", '"': '"', '[': "]"},
				line_comment='--',
				block_comments=['/*', '*/'],
				operators1char=frozenset('><=-+*/%&|^~'),
				operators2chars=frozenset(['<>', '<=', '>='])				 
				 )
	buf:list[TSqlToken] = []

	for t in it:
		token = TSqlToken(t)
		token.value = token.get_value(sql)
		if token.type == tokenizer.WORD or token.value == '.':
			buf.append(token)
			continue
		yield from _flush_buffer(buf)
		yield token
	
	yield from _flush_buffer(buf=buf)
