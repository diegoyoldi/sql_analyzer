import string
from dataclasses import dataclass
from typing import Iterator, Dict, List
import tokenizer
from enum import IntEnum

class EnumTokenType(IntEnum):
	UNKNOWN = 0
	WORD = 1
	NUMBER = 2
	DELIMITED_LITERAL = 3
	OPERATOR = 4
	DELIMITER = 5	
	KEYWORD = 6
	IDENTIFIER = 7
	
class EnumTokenSubtype(IntEnum):
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
	
@dataclass
class TSqlToken(tokenizer.Token):
	value:str
	subtype:EnumTokenSubtype
	is_starter_keyword:bool	
	def __init__(self, token:tokenizer.Token):
		self.start = token.start
		self.end = token.end
		self.type = EnumTokenType(token.type)
		self.subtype = None
		self.is_starter_keyword = None
	def __str__(self):
		return self.value

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

STARTER_KEYWORDS_1 = frozenset({
	'SELECT', 'UPDATE', 'INSERT', 'DELETE', 'MERGE', 'CREATE', 'DROP', 'TRUNCATE', 'ALTER', 'EXEC', 'EXECUTE', 
	'DECLARE', 'SET', 'COMMIT', 'ROLLBACK', 'USE', 'GRANT', 'DENY', 'REVOKE', 'SAVE', 'BACKUP', 
	'RESTORE', 'PRINT', 'GOTO', 'RETURN', 'IF', 'WHILE'
})

STARTER_KEYWORDS_2 = frozenset({
	'BEGIN TRAN', 'BEGIN TRANSACTION', 'COMMIT TRAN', 'COMMIT TRANSACTION'
})

_KEYWORD_SUBTYPES_1 = {'SESSION_USER': EnumTokenSubtype.UNKNOWN, 'VIEW': EnumTokenSubtype.UNKNOWN, 'NOT': EnumTokenSubtype.UNKNOWN, 'TSEQUAL': EnumTokenSubtype.UNKNOWN, 'SECURITYAUDIT': EnumTokenSubtype.UNKNOWN, 'CONVERT': EnumTokenSubtype.UNKNOWN, 'BROWSE': EnumTokenSubtype.UNKNOWN, 'UNPIVOT': EnumTokenSubtype.UNKNOWN, 'ROWCOUNT': EnumTokenSubtype.UNKNOWN, 'RETURN': EnumTokenSubtype.FLOW_CONTROL, 'SEMANTICSIMILARITYDETAILSTABLE': EnumTokenSubtype.UNKNOWN, 'PROCEDURE': EnumTokenSubtype.UNKNOWN, 'DENY': EnumTokenSubtype.DCL, 'PIVOT': EnumTokenSubtype.UNKNOWN, 'AND': EnumTokenSubtype.UNKNOWN, 'TOP': EnumTokenSubtype.QUERY_CLAUSES, 'INTO': EnumTokenSubtype.UNKNOWN, 'SET': EnumTokenSubtype.OTHER_KEYWORDS, 'END': EnumTokenSubtype.UNKNOWN, 'CASE': EnumTokenSubtype.FLOW_CONTROL, 'CHECK': EnumTokenSubtype.UNKNOWN, 'COLUMN': EnumTokenSubtype.UNKNOWN, 'EXECUTE': EnumTokenSubtype.UNKNOWN, 'DISK': EnumTokenSubtype.UNKNOWN, 'MERGE': EnumTokenSubtype.DML, 'INNER': EnumTokenSubtype.UNKNOWN, 'NATIONAL': EnumTokenSubtype.UNKNOWN, 'ERRLVL': EnumTokenSubtype.UNKNOWN, 'TEXTSIZE': EnumTokenSubtype.UNKNOWN, 'DROP': EnumTokenSubtype.DDL, 'USER': EnumTokenSubtype.UNKNOWN, 'DBCC': EnumTokenSubtype.UNKNOWN, 'AS': EnumTokenSubtype.UNKNOWN, 'HAVING': EnumTokenSubtype.QUERY_CLAUSES, 'BACKUP': EnumTokenSubtype.UNKNOWN, 'WHEN': EnumTokenSubtype.UNKNOWN, 'CURRENT_TIME': EnumTokenSubtype.UNKNOWN, 'OPTION': EnumTokenSubtype.OTHER_KEYWORDS, 'SHUTDOWN': EnumTokenSubtype.UNKNOWN, 'CLOSE': EnumTokenSubtype.UNKNOWN, 'IDENTITY': EnumTokenSubtype.UNKNOWN, 'IS': EnumTokenSubtype.UNKNOWN, 'NOCHECK': EnumTokenSubtype.UNKNOWN, 'PRECISION': EnumTokenSubtype.UNKNOWN, 'FOR': EnumTokenSubtype.UNKNOWN, 'PUBLIC': EnumTokenSubtype.UNKNOWN, 'OR': EnumTokenSubtype.UNKNOWN, 'THEN': EnumTokenSubtype.UNKNOWN, 'FREETEXT': EnumTokenSubtype.UNKNOWN, 'CURSOR': EnumTokenSubtype.UNKNOWN, 'REFERENCES': EnumTokenSubtype.UNKNOWN, 'DECLARE': EnumTokenSubtype.OTHER_KEYWORDS, 'CURRENT_DATE': EnumTokenSubtype.UNKNOWN, 'FREETEXTTABLE': EnumTokenSubtype.UNKNOWN, 'CROSS': EnumTokenSubtype.UNKNOWN, 'TRIGGER': EnumTokenSubtype.UNKNOWN, 'CURRENT': EnumTokenSubtype.UNKNOWN, 'BETWEEN': EnumTokenSubtype.UNKNOWN, 'LIKE': EnumTokenSubtype.UNKNOWN, 'EXEC': EnumTokenSubtype.OTHER_KEYWORDS, 'GOTO': EnumTokenSubtype.FLOW_CONTROL, 'CONTINUE': EnumTokenSubtype.FLOW_CONTROL, 'ESCAPE': EnumTokenSubtype.UNKNOWN, 'NULLIF': EnumTokenSubtype.UNKNOWN, 'NONCLUSTERED': EnumTokenSubtype.UNKNOWN, 'FILE': EnumTokenSubtype.UNKNOWN, 'ON': EnumTokenSubtype.UNKNOWN, 'RECONFIGURE': EnumTokenSubtype.UNKNOWN, 'COMMIT': EnumTokenSubtype.TCL, 'COLLATE': EnumTokenSubtype.UNKNOWN, 'OVER': EnumTokenSubtype.UNKNOWN, 'SEMANTICSIMILARITYTABLE': EnumTokenSubtype.UNKNOWN, 'FETCH': EnumTokenSubtype.UNKNOWN, 'SEMANTICKEYPHRASETABLE': EnumTokenSubtype.UNKNOWN, 'TABLESAMPLE': EnumTokenSubtype.UNKNOWN, 'FILLFACTOR': EnumTokenSubtype.UNKNOWN, 'DATABASE': EnumTokenSubtype.UNKNOWN, 'DELETE': EnumTokenSubtype.DML, 'OPENDATASOURCE': EnumTokenSubtype.UNKNOWN, 'RESTORE': EnumTokenSubtype.UNKNOWN, 'IDENTITY_INSERT': EnumTokenSubtype.UNKNOWN, 'KILL': EnumTokenSubtype.UNKNOWN, 'INTERSECT': EnumTokenSubtype.SET_OPERATORS, 'GRANT': EnumTokenSubtype.DCL, 'CONTAINSTABLE': EnumTokenSubtype.UNKNOWN, 'FROM': EnumTokenSubtype.QUERY_CLAUSES, 'VALUES': EnumTokenSubtype.UNKNOWN, 'TRY_CONVERT': EnumTokenSubtype.UNKNOWN, 'EXIT': EnumTokenSubtype.UNKNOWN, 'DOUBLE': EnumTokenSubtype.UNKNOWN, 'CURRENT_TIMESTAMP': EnumTokenSubtype.UNKNOWN, 'PROC': EnumTokenSubtype.UNKNOWN, 'EXCEPT': EnumTokenSubtype.SET_OPERATORS, 'HOLDLOCK': EnumTokenSubtype.UNKNOWN, 'WHERE': EnumTokenSubtype.QUERY_CLAUSES, 'PLAN': EnumTokenSubtype.UNKNOWN, 'TABLE': EnumTokenSubtype.UNKNOWN, 'CONTAINS': EnumTokenSubtype.UNKNOWN, 'REVOKE': EnumTokenSubtype.DCL, 'REPLICATION': EnumTokenSubtype.UNKNOWN, 'ASC': EnumTokenSubtype.UNKNOWN, 'TRUNCATE': EnumTokenSubtype.DDL, 'IN': EnumTokenSubtype.SET_PREDICATE_OPERATORS, 'ADD': EnumTokenSubtype.UNKNOWN, 'READTEXT': EnumTokenSubtype.UNKNOWN, 'REVERT': EnumTokenSubtype.UNKNOWN, 'COALESCE': EnumTokenSubtype.UNKNOWN, 'USE': EnumTokenSubtype.OTHER_KEYWORDS, 'CURRENT_USER': EnumTokenSubtype.UNKNOWN, 'OPENQUERY': EnumTokenSubtype.UNKNOWN, 'LOAD': EnumTokenSubtype.UNKNOWN, 'OF': EnumTokenSubtype.UNKNOWN, 'DUMP': EnumTokenSubtype.UNKNOWN, 'LINENO': EnumTokenSubtype.UNKNOWN, 'EXISTS': EnumTokenSubtype.SET_PREDICATE_OPERATORS, 'OFF': EnumTokenSubtype.UNKNOWN, 'UNION': EnumTokenSubtype.SET_OPERATORS, 'DISTRIBUTED': EnumTokenSubtype.UNKNOWN, 'VARYING': EnumTokenSubtype.UNKNOWN, 'DESC': EnumTokenSubtype.UNKNOWN, 'SYSTEM_USER': EnumTokenSubtype.UNKNOWN, 'IF': EnumTokenSubtype.FLOW_CONTROL, 'ELSE': EnumTokenSubtype.FLOW_CONTROL, 'OPENXML': EnumTokenSubtype.UNKNOWN, 'SETUSER': EnumTokenSubtype.UNKNOWN, 'CLUSTERED': EnumTokenSubtype.UNKNOWN, 'WHILE': EnumTokenSubtype.FLOW_CONTROL, 'WITH': EnumTokenSubtype.OTHER_KEYWORDS, 'LEFT': EnumTokenSubtype.UNKNOWN, 'ROLLBACK': EnumTokenSubtype.TCL, 'WAITFOR': EnumTokenSubtype.UNKNOWN, 'SCHEMA': EnumTokenSubtype.UNKNOWN, 'DISTINCT': EnumTokenSubtype.UNKNOWN, 'BULK': EnumTokenSubtype.UNKNOWN, 'FUNCTION': EnumTokenSubtype.UNKNOWN, 'SAVE': EnumTokenSubtype.UNKNOWN, 'CONSTRAINT': EnumTokenSubtype.UNKNOWN, 'UPDATETEXT': EnumTokenSubtype.UNKNOWN, 'CASCADE': EnumTokenSubtype.UNKNOWN, 'FOREIGN': EnumTokenSubtype.UNKNOWN, 'OPEN': EnumTokenSubtype.UNKNOWN, 'ALL': EnumTokenSubtype.SET_PREDICATE_OPERATORS, 'BREAK': EnumTokenSubtype.FLOW_CONTROL, 'ROWGUIDCOL': EnumTokenSubtype.UNKNOWN, 'TRANSACTION': EnumTokenSubtype.UNKNOWN, 'UPDATE': EnumTokenSubtype.DML, 'ANY': EnumTokenSubtype.SET_PREDICATE_OPERATORS, 'BY': EnumTokenSubtype.UNKNOWN, 'ORDER': EnumTokenSubtype.UNKNOWN, 'EXTERNAL': EnumTokenSubtype.UNKNOWN, 'KEY': EnumTokenSubtype.UNKNOWN, 'TRAN': EnumTokenSubtype.UNKNOWN, 'OFFSETS': EnumTokenSubtype.UNKNOWN, 'RAISERROR': EnumTokenSubtype.UNKNOWN, 'SELECT': EnumTokenSubtype.QUERY_CLAUSES, 'CREATE': EnumTokenSubtype.DDL, 'GROUP': EnumTokenSubtype.UNKNOWN, 'FULL': EnumTokenSubtype.UNKNOWN, 'ALTER': EnumTokenSubtype.DDL, 'READ': EnumTokenSubtype.UNKNOWN, 'INSERT': EnumTokenSubtype.DML, 'BEGIN': EnumTokenSubtype.UNKNOWN, 'STATISTICS': EnumTokenSubtype.UNKNOWN, 'OUTER': EnumTokenSubtype.UNKNOWN, 'OPENROWSET': EnumTokenSubtype.UNKNOWN, 'SOME': EnumTokenSubtype.SET_PREDICATE_OPERATORS, 'RULE': EnumTokenSubtype.UNKNOWN, 'AUTHORIZATION': EnumTokenSubtype.UNKNOWN, 'PRINT': EnumTokenSubtype.OTHER_KEYWORDS, 'DEALLOCATE': EnumTokenSubtype.UNKNOWN, 'PERCENT': EnumTokenSubtype.UNKNOWN, 'RIGHT': EnumTokenSubtype.UNKNOWN, 'INDEX': EnumTokenSubtype.UNKNOWN, 'JOIN': EnumTokenSubtype.RELATIONAL_OPERATORS, 'PRIMARY': EnumTokenSubtype.UNKNOWN, 'UNIQUE': EnumTokenSubtype.UNKNOWN, 'WRITETEXT': EnumTokenSubtype.UNKNOWN, 'COMPUTE': EnumTokenSubtype.UNKNOWN, 'RESTRICT': EnumTokenSubtype.UNKNOWN, 'TO': EnumTokenSubtype.UNKNOWN, 'DEFAULT': EnumTokenSubtype.UNKNOWN, 'NULL': EnumTokenSubtype.UNKNOWN, 'CHECKPOINT': EnumTokenSubtype.UNKNOWN, 'IDENTITYCOL': EnumTokenSubtype.UNKNOWN}
_KEYWORD_SUBTYPES_2 = {('INNER', 'JOIN'): ['INNER JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('CROSS', 'JOIN'): ['CROSS JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('COMMIT', 'TRAN'): ['COMMIT TRAN', None], ('ADD', 'CONSTRAINT'): ['ADD CONSTRAINT', None], ('WITHIN', 'GROUP'): ['WITHIN GROUP', None], ('BEGIN', 'TRAN'): ['BEGIN TRAN', None], ('CROSS', 'APPLY'): ['CROSS APPLY', None], ('BEGIN', 'TRANSACTION'): ['BEGIN TRANSACTION', EnumTokenSubtype.TCL], ('ROLLBACK', 'TRANSACTION'): ['ROLLBACK TRANSACTION', None], ('BEGIN', 'TRY'): ['BEGIN TRY', None], ('GROUP', 'BY'): ['GROUP BY', EnumTokenSubtype.QUERY_CLAUSES], ('END', 'CATCH'): ['END CATCH', None], ('FULL', 'JOIN'): ['FULL JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('COMMIT', 'TRANSACTION'): ['COMMIT TRANSACTION', None], ('ADD', 'COLUMN'): ['ADD COLUMN', None], ('BEGIN', 'CATCH'): ['BEGIN CATCH', None], ('LEFT', 'JOIN'): ['LEFT JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('ROLLBACK', 'TRAN'): ['ROLLBACK TRAN', None], ('ORDER', 'BY'): ['ORDER BY', EnumTokenSubtype.QUERY_CLAUSES], ('END', 'TRY'): ['END TRY', None], ('RIGHT', 'JOIN'): ['RIGHT JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('OUTER', 'APPLY'): ['OUTER APPLY', None], ('IS', 'NULL'): ['IS NULL', None]}
_KEYWORD_SUBTYPES_3 = {('RIGHT', 'OUTER', 'JOIN'): ['RIGHT OUTER JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('LEFT', 'OUTER', 'JOIN'): ['LEFT OUTER JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('FULL', 'OUTER', 'JOIN'): ['FULL OUTER JOIN', EnumTokenSubtype.RELATIONAL_OPERATORS], ('IS', 'NOT', 'NULL'): ['IS NOT NULL', None]}

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
			buf[i].type = EnumTokenType.KEYWORD.value
			buf[i].subtype = subtype[1]
			del buf[i+1:i+3]
		elif pending >= 2 and (subtype := _KEYWORD_SUBTYPES_2.get((buf[i].value.upper(), buf[i+1].value.upper()))) != None:
			buf[i].value = subtype[0]
			buf[i].end = buf[i+1].end
			buf[i].type = EnumTokenType.KEYWORD.value
			buf[i].subtype = subtype[1]
			buf[i].is_starter_keyword = buf[i].value in STARTER_KEYWORDS_2
			del buf[i+1:i+2]
		elif (subtype := _KEYWORD_SUBTYPES_1.get(buf[i].value.upper())) != None:
			buf[i].value = buf[i].value.upper()
			buf[i].type = EnumTokenType.KEYWORD.value
			buf[i].subtype = subtype
			buf[i].is_starter_keyword = buf[i].value in STARTER_KEYWORDS_1
		i += 1

	while buf:
		# Merge dotted identifiers
		if buf[0].type == EnumTokenType.WORD.value:
			buf[0].type = EnumTokenType.IDENTIFIER.value
			c = buf[0].value[0]
			if c == '@': buf[0].subtype = EnumTokenSubtype.VARIABLE
			elif c == '#': buf[0].subtype = EnumTokenSubtype.TEMPORARY_OBJECT
			while len(buf) >= 3 and buf[1].value == '.' and buf[2].type != EnumTokenType.KEYWORD.value:
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
