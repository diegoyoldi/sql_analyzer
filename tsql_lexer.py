import string
from typing import Iterator, List
from tokenizer import Token, tokenize, EnumTokenType
from enum import IntEnum, auto

class EnumValueId(IntEnum):
	RIGHT_OUTER_JOIN = auto()
	LEFT_OUTER_JOIN = auto()
	FULL_OUTER_JOIN = auto()
	IS_NOT_NULL = auto()
	INNER_JOIN = auto()
	CROSS_JOIN = auto()
	COMMIT_TRAN = auto()
	ADD_CONSTRAINT = auto()
	WITHIN_GROUP = auto()
	BEGIN_TRAN = auto()
	CROSS_APPLY = auto()
	BEGIN_TRANSACTION = auto()
	ROLLBACK_TRANSACTION = auto()
	BEGIN_TRY = auto()
	GROUP_BY = auto()
	END_CATCH = auto()
	FULL_JOIN = auto()
	COMMIT_TRANSACTION = auto()
	ADD_COLUMN = auto()
	BEGIN_CATCH = auto()
	LEFT_JOIN = auto()
	ROLLBACK_TRAN = auto()
	ORDER_BY = auto()
	END_TRY = auto()
	RIGHT_JOIN = auto()
	OUTER_APPLY = auto()
	IS_NULL = auto()
	NOT_IN = auto()
	NOT_BETWEEN = auto()
	NOT_LIKE = auto()
	NOT_EXISTS = auto()
	SESSION_USER = auto()
	VIEW = auto()
	NOT = auto()
	TSEQUAL = auto()
	SECURITYAUDIT = auto()
	CONVERT = auto()
	BROWSE = auto()
	UNPIVOT = auto()
	ROWCOUNT = auto()
	RETURN = auto()
	SEMANTICSIMILARITYDETAILSTABLE = auto()
	PROCEDURE = auto()
	DENY = auto()
	PIVOT = auto()
	AND = auto()
	TOP = auto()
	INTO = auto()
	SET = auto()
	END = auto()
	CASE = auto()
	CHECK = auto()
	COLUMN = auto()
	EXECUTE = auto()
	DISK = auto()
	MERGE = auto()
	INNER = auto()
	NATIONAL = auto()
	ERRLVL = auto()
	TEXTSIZE = auto()
	DROP = auto()
	USER = auto()
	DBCC = auto()
	AS = auto()
	HAVING = auto()
	BACKUP = auto()
	WHEN = auto()
	CURRENT_TIME = auto()
	OPTION = auto()
	SHUTDOWN = auto()
	CLOSE = auto()
	IDENTITY = auto()
	IS = auto()
	NOCHECK = auto()
	PRECISION = auto()
	FOR = auto()
	PUBLIC = auto()
	OR = auto()
	THEN = auto()
	FREETEXT = auto()
	REFERENCES = auto()
	DECLARE = auto()
	CURRENT_DATE = auto()
	FREETEXTTABLE = auto()
	CROSS = auto()
	TRIGGER = auto()
	CURRENT = auto()
	BETWEEN = auto()
	LIKE = auto()
	EXEC = auto()
	GOTO = auto()
	CONTINUE = auto()
	ESCAPE = auto()
	NULLIF = auto()
	NONCLUSTERED = auto()
	FILE = auto()
	ON = auto()
	RECONFIGURE = auto()
	COMMIT = auto()
	COLLATE = auto()
	OVER = auto()
	SEMANTICSIMILARITYTABLE = auto()
	FETCH = auto()
	SEMANTICKEYPHRASETABLE = auto()
	TABLESAMPLE = auto()
	FILLFACTOR = auto()
	DATABASE = auto()
	DELETE = auto()
	OPENDATASOURCE = auto()
	RESTORE = auto()
	IDENTITY_INSERT = auto()
	KILL = auto()
	INTERSECT = auto()
	GRANT = auto()
	CONTAINSTABLE = auto()
	FROM = auto()
	VALUES = auto()
	TRY_CONVERT = auto()
	EXIT = auto()
	DOUBLE = auto()
	CURRENT_TIMESTAMP = auto()
	PROC = auto()
	EXCEPT = auto()
	HOLDLOCK = auto()
	WHERE = auto()
	PLAN = auto()
	TABLE = auto()
	CONTAINS = auto()
	REVOKE = auto()
	REPLICATION = auto()
	ASC = auto()
	TRUNCATE = auto()
	IN = auto()
	ADD = auto()
	READTEXT = auto()
	REVERT = auto()
	COALESCE = auto()
	USE = auto()
	CURRENT_USER = auto()
	OPENQUERY = auto()
	LOAD = auto()
	OF = auto()
	DUMP = auto()
	LINENO = auto()
	EXISTS = auto()
	OFF = auto()
	UNION = auto()
	DISTRIBUTED = auto()
	VARYING = auto()
	DESC = auto()
	SYSTEM_USER = auto()
	IF = auto()
	ELSE = auto()
	OPENXML = auto()
	SETUSER = auto()
	CLUSTERED = auto()
	WHILE = auto()
	WITH = auto()
	LEFT = auto()
	ROLLBACK = auto()
	WAITFOR = auto()
	SCHEMA = auto()
	DISTINCT = auto()
	BULK = auto()
	FUNCTION = auto()
	SAVE = auto()
	CONSTRAINT = auto()
	UPDATETEXT = auto()
	CASCADE = auto()
	FOREIGN = auto()
	OPEN = auto()
	ALL = auto()
	BREAK = auto()
	ROWGUIDCOL = auto()
	TRANSACTION = auto()
	UPDATE = auto()
	ANY = auto()
	BY = auto()
	ORDER = auto()
	EXTERNAL = auto()
	KEY = auto()
	TRAN = auto()
	OFFSETS = auto()
	RAISERROR = auto()
	SELECT = auto()
	CREATE = auto()
	GROUP = auto()
	FULL = auto()
	ALTER = auto()
	READ = auto()
	INSERT = auto()
	BEGIN = auto()
	STATISTICS = auto()
	OUTER = auto()
	OPENROWSET = auto()
	SOME = auto()
	RULE = auto()
	AUTHORIZATION = auto()
	PRINT = auto()
	DEALLOCATE = auto()
	PERCENT = auto()
	RIGHT = auto()
	INDEX = auto()
	JOIN = auto()
	PRIMARY = auto()
	UNIQUE = auto()
	WRITETEXT = auto()
	COMPUTE = auto()
	RESTRICT = auto()
	TO = auto()
	DEFAULT = auto()
	NULL = auto()
	CHECKPOINT = auto()
	IDENTITYCOL = auto()

	#Not Keyword
	WITHIN = auto()
	APPLY = auto()
	TRY = auto()
	CATCH = auto()
	PARTITION = auto()
	ROW = auto()
	ROWS = auto()
	RANGE = auto()
	UNBOUNDED = auto()
	PRECEDING = auto()
	FOLLOWING = auto()
	PATH = auto()
	AUTO = auto()
	EXPLICIT = auto()
	RAW = auto()
	ABSENT = auto()
	XSINIL = auto()
	ELEMENTS = auto()
	XMLSCHEMA = auto()
	XMLDATA = auto()
	ROOT = auto()
	INCLUDE_NULL_VALUES = auto()
	WITHOUT_ARRAY_WRAPPER = auto()
	OPENJSON = auto()
	BINARY = auto()
	BASE64 = auto()
	TYPE = auto()
	OFFSET = auto()
	ONLY = auto()
	TIES = auto()
	CAST = auto()
	AVG = auto()
	COUNT = auto()
	SUM = auto()
	MIN = auto()
	MAX = auto()

	# Data types - Exact
	TINYINT = auto()
	SMALLINT = auto()
	INT = auto()
	BIGINT = auto()
	BIT = auto()
	DECIMAL = auto()
	NUMERIC = auto()
	MONEY = auto()
	SMALLMONEY = auto()

	# Data types - Approximate
	FLOAT = auto()
	REAL = auto()

	# Data types - Date and time
	DATE = auto()
	TIME = auto()
	DATETIME2 = auto()
	DATETIMEOFFSET = auto()
	DATETIME = auto()
	SMALLDATETIME = auto()

	# Data types - Character string
	CHAR = auto()
	VARCHAR = auto()
	TEXT = auto()

	# Data types - Unicode character string
	NCHAR = auto()
	NVARCHAR = auto()
	NTEXT = auto()

	# Data types - Binary strings
	# BINARY = auto()
	VARBINARY = auto()
	IMAGE = auto()

	# Data types - Other data types
	CURSOR = auto()
	GEOGRAPHY = auto()
	GEOMETRY = auto()
	HIERARCHYID = auto()
	JSON = auto()
	VECTOR = auto()
	ROWVERSION = auto()
	SQL_VARIANT = auto()
	# TABLE = auto()
	UNIQUEIDENTIFIER = auto()
	XML = auto()

	# Comparision
	EQ = auto()
	NE = auto()
	GT = auto()
	GE = auto()
	LT = auto()
	LE = auto()
	
	# Arithmetic
	OP_ADD = auto()
	OP_SUB = auto()
	OP_MUL = auto()
	OP_DIV = auto()
	OP_MOD = auto()
	# Parentheses
	PARENTH_1 = auto()
	PARENTH_2 = auto()

	# Bitwise
	BW_AND = auto()
	BW_OR = auto()
	BW_XOR = auto()
	BW_NOT = auto()

	# Delimiters
	SEMICOLON = auto()
	COMMA = auto()
	DOT = auto()

value_hash = {
	'SESSION_USER': EnumValueId.SESSION_USER,
	'VIEW': EnumValueId.VIEW,
	'NOT': EnumValueId.NOT,
	'TSEQUAL': EnumValueId.TSEQUAL,
	'SECURITYAUDIT': EnumValueId.SECURITYAUDIT,
	'CONVERT': EnumValueId.CONVERT,
	'BROWSE': EnumValueId.BROWSE,
	'UNPIVOT': EnumValueId.UNPIVOT,
	'ROWCOUNT': EnumValueId.ROWCOUNT,
	'RETURN': EnumValueId.RETURN,
	'SEMANTICSIMILARITYDETAILSTABLE': EnumValueId.SEMANTICSIMILARITYDETAILSTABLE,
	'PROCEDURE': EnumValueId.PROCEDURE,
	'DENY': EnumValueId.DENY,
	'PIVOT': EnumValueId.PIVOT,
	'AND': EnumValueId.AND,
	'TOP': EnumValueId.TOP,
	'INTO': EnumValueId.INTO,
	'SET': EnumValueId.SET,
	'END': EnumValueId.END,
	'CASE': EnumValueId.CASE,
	'CHECK': EnumValueId.CHECK,
	'COLUMN': EnumValueId.COLUMN,
	'EXECUTE': EnumValueId.EXECUTE,
	'DISK': EnumValueId.DISK,
	'MERGE': EnumValueId.MERGE,
	'INNER': EnumValueId.INNER,
	'NATIONAL': EnumValueId.NATIONAL,
	'ERRLVL': EnumValueId.ERRLVL,
	'TEXTSIZE': EnumValueId.TEXTSIZE,
	'DROP': EnumValueId.DROP,
	'USER': EnumValueId.USER,
	'DBCC': EnumValueId.DBCC,
	'AS': EnumValueId.AS,
	'HAVING': EnumValueId.HAVING,
	'BACKUP': EnumValueId.BACKUP,
	'WHEN': EnumValueId.WHEN,
	'CURRENT_TIME': EnumValueId.CURRENT_TIME,
	'OPTION': EnumValueId.OPTION,
	'SHUTDOWN': EnumValueId.SHUTDOWN,
	'CLOSE': EnumValueId.CLOSE,
	'IDENTITY': EnumValueId.IDENTITY,
	'IS': EnumValueId.IS,
	'NOCHECK': EnumValueId.NOCHECK,
	'PRECISION': EnumValueId.PRECISION,
	'FOR': EnumValueId.FOR,
	'PUBLIC': EnumValueId.PUBLIC,
	'OR': EnumValueId.OR,
	'THEN': EnumValueId.THEN,
	'FREETEXT': EnumValueId.FREETEXT,
	'CURSOR': EnumValueId.CURSOR,
	'REFERENCES': EnumValueId.REFERENCES,
	'DECLARE': EnumValueId.DECLARE,
	'CURRENT_DATE': EnumValueId.CURRENT_DATE,
	'FREETEXTTABLE': EnumValueId.FREETEXTTABLE,
	'CROSS': EnumValueId.CROSS,
	'TRIGGER': EnumValueId.TRIGGER,
	'CURRENT': EnumValueId.CURRENT,
	'BETWEEN': EnumValueId.BETWEEN,
	'LIKE': EnumValueId.LIKE,
	'EXEC': EnumValueId.EXEC,
	'GOTO': EnumValueId.GOTO,
	'CONTINUE': EnumValueId.CONTINUE,
	'ESCAPE': EnumValueId.ESCAPE,
	'NULLIF': EnumValueId.NULLIF,
	'NONCLUSTERED': EnumValueId.NONCLUSTERED,
	'FILE': EnumValueId.FILE,
	'ON': EnumValueId.ON,
	'RECONFIGURE': EnumValueId.RECONFIGURE,
	'COMMIT': EnumValueId.COMMIT,
	'COLLATE': EnumValueId.COLLATE,
	'OVER': EnumValueId.OVER,
	'SEMANTICSIMILARITYTABLE': EnumValueId.SEMANTICSIMILARITYTABLE,
	'FETCH': EnumValueId.FETCH,
	'SEMANTICKEYPHRASETABLE': EnumValueId.SEMANTICKEYPHRASETABLE,
	'TABLESAMPLE': EnumValueId.TABLESAMPLE,
	'FILLFACTOR': EnumValueId.FILLFACTOR,
	'DATABASE': EnumValueId.DATABASE,
	'DELETE': EnumValueId.DELETE,
	'OPENDATASOURCE': EnumValueId.OPENDATASOURCE,
	'RESTORE': EnumValueId.RESTORE,
	'IDENTITY_INSERT': EnumValueId.IDENTITY_INSERT,
	'KILL': EnumValueId.KILL,
	'INTERSECT': EnumValueId.INTERSECT,
	'GRANT': EnumValueId.GRANT,
	'CONTAINSTABLE': EnumValueId.CONTAINSTABLE,
	'FROM': EnumValueId.FROM,
	'VALUES': EnumValueId.VALUES,
	'TRY_CONVERT': EnumValueId.TRY_CONVERT,
	'EXIT': EnumValueId.EXIT,
	'DOUBLE': EnumValueId.DOUBLE,
	'CURRENT_TIMESTAMP': EnumValueId.CURRENT_TIMESTAMP,
	'PROC': EnumValueId.PROC,
	'EXCEPT': EnumValueId.EXCEPT,
	'HOLDLOCK': EnumValueId.HOLDLOCK,
	'WHERE': EnumValueId.WHERE,
	'PLAN': EnumValueId.PLAN,
	'TABLE': EnumValueId.TABLE,
	'CONTAINS': EnumValueId.CONTAINS,
	'REVOKE': EnumValueId.REVOKE,
	'REPLICATION': EnumValueId.REPLICATION,
	'ASC': EnumValueId.ASC,
	'TRUNCATE': EnumValueId.TRUNCATE,
	'IN': EnumValueId.IN,
	'ADD': EnumValueId.ADD,
	'READTEXT': EnumValueId.READTEXT,
	'REVERT': EnumValueId.REVERT,
	'COALESCE': EnumValueId.COALESCE,
	'USE': EnumValueId.USE,
	'CURRENT_USER': EnumValueId.CURRENT_USER,
	'OPENQUERY': EnumValueId.OPENQUERY,
	'LOAD': EnumValueId.LOAD,
	'OF': EnumValueId.OF,
	'DUMP': EnumValueId.DUMP,
	'LINENO': EnumValueId.LINENO,
	'EXISTS': EnumValueId.EXISTS,
	'OFF': EnumValueId.OFF,
	'UNION': EnumValueId.UNION,
	'DISTRIBUTED': EnumValueId.DISTRIBUTED,
	'VARYING': EnumValueId.VARYING,
	'DESC': EnumValueId.DESC,
	'SYSTEM_USER': EnumValueId.SYSTEM_USER,
	'IF': EnumValueId.IF,
	'ELSE': EnumValueId.ELSE,
	'OPENXML': EnumValueId.OPENXML,
	'SETUSER': EnumValueId.SETUSER,
	'CLUSTERED': EnumValueId.CLUSTERED,
	'WHILE': EnumValueId.WHILE,
	'WITH': EnumValueId.WITH,
	'LEFT': EnumValueId.LEFT,
	'ROLLBACK': EnumValueId.ROLLBACK,
	'WAITFOR': EnumValueId.WAITFOR,
	'SCHEMA': EnumValueId.SCHEMA,
	'DISTINCT': EnumValueId.DISTINCT,
	'BULK': EnumValueId.BULK,
	'FUNCTION': EnumValueId.FUNCTION,
	'SAVE': EnumValueId.SAVE,
	'CONSTRAINT': EnumValueId.CONSTRAINT,
	'UPDATETEXT': EnumValueId.UPDATETEXT,
	'CASCADE': EnumValueId.CASCADE,
	'FOREIGN': EnumValueId.FOREIGN,
	'OPEN': EnumValueId.OPEN,
	'ALL': EnumValueId.ALL,
	'BREAK': EnumValueId.BREAK,
	'ROWGUIDCOL': EnumValueId.ROWGUIDCOL,
	'TRANSACTION': EnumValueId.TRANSACTION,
	'UPDATE': EnumValueId.UPDATE,
	'ANY': EnumValueId.ANY,
	'BY': EnumValueId.BY,
	'ORDER': EnumValueId.ORDER,
	'EXTERNAL': EnumValueId.EXTERNAL,
	'KEY': EnumValueId.KEY,
	'TRAN': EnumValueId.TRAN,
	'OFFSETS': EnumValueId.OFFSETS,
	'RAISERROR': EnumValueId.RAISERROR,
	'SELECT': EnumValueId.SELECT,
	'CREATE': EnumValueId.CREATE,
	'GROUP': EnumValueId.GROUP,
	'FULL': EnumValueId.FULL,
	'ALTER': EnumValueId.ALTER,
	'READ': EnumValueId.READ,
	'INSERT': EnumValueId.INSERT,
	'BEGIN': EnumValueId.BEGIN,
	'STATISTICS': EnumValueId.STATISTICS,
	'OUTER': EnumValueId.OUTER,
	'OPENROWSET': EnumValueId.OPENROWSET,
	'SOME': EnumValueId.SOME,
	'RULE': EnumValueId.RULE,
	'AUTHORIZATION': EnumValueId.AUTHORIZATION,
	'PRINT': EnumValueId.PRINT,
	'DEALLOCATE': EnumValueId.DEALLOCATE,
	'PERCENT': EnumValueId.PERCENT,
	'RIGHT': EnumValueId.RIGHT,
	'INDEX': EnumValueId.INDEX,
	'JOIN': EnumValueId.JOIN,
	'PRIMARY': EnumValueId.PRIMARY,
	'UNIQUE': EnumValueId.UNIQUE,
	'WRITETEXT': EnumValueId.WRITETEXT,
	'COMPUTE': EnumValueId.COMPUTE,
	'RESTRICT': EnumValueId.RESTRICT,
	'TO': EnumValueId.TO,
	'DEFAULT': EnumValueId.DEFAULT,
	'NULL': EnumValueId.NULL,
	'CHECKPOINT': EnumValueId.CHECKPOINT,
	'IDENTITYCOL': EnumValueId.IDENTITYCOL,
	'INNER JOIN': EnumValueId.INNER_JOIN,
	'CROSS JOIN': EnumValueId.CROSS_JOIN,
	'COMMIT TRAN': EnumValueId.COMMIT_TRAN,
	'ADD CONSTRAINT': EnumValueId.ADD_CONSTRAINT,
	'WITHIN GROUP': EnumValueId.WITHIN_GROUP,
	'BEGIN TRAN': EnumValueId.BEGIN_TRAN,
	'CROSS APPLY': EnumValueId.CROSS_APPLY,
	'BEGIN TRANSACTION': EnumValueId.BEGIN_TRANSACTION,
	'ROLLBACK TRANSACTION': EnumValueId.ROLLBACK_TRANSACTION,
	'BEGIN TRY': EnumValueId.BEGIN_TRY,
	'GROUP BY': EnumValueId.GROUP_BY,
	'END CATCH': EnumValueId.END_CATCH,
	'FULL JOIN': EnumValueId.FULL_JOIN,
	'COMMIT TRANSACTION': EnumValueId.COMMIT_TRANSACTION,
	'ADD COLUMN': EnumValueId.ADD_COLUMN,
	'BEGIN CATCH': EnumValueId.BEGIN_CATCH,
	'LEFT JOIN': EnumValueId.LEFT_JOIN,
	'ROLLBACK TRAN': EnumValueId.ROLLBACK_TRAN,
	'ORDER BY': EnumValueId.ORDER_BY,
	'END TRY': EnumValueId.END_TRY,
	'RIGHT JOIN': EnumValueId.RIGHT_JOIN,
	'OUTER APPLY': EnumValueId.OUTER_APPLY,
	'IS NULL': EnumValueId.IS_NULL,
	'NOT IN': EnumValueId.NOT_IN,
	'NOT BETWEEN': EnumValueId.NOT_BETWEEN,
	'NOT LIKE': EnumValueId.NOT_LIKE,
	'NOT EXISTS': EnumValueId.NOT_EXISTS,
	'RIGHT OUTER JOIN': EnumValueId.RIGHT_OUTER_JOIN,
	'LEFT OUTER JOIN': EnumValueId.LEFT_OUTER_JOIN,
	'FULL OUTER JOIN': EnumValueId.FULL_OUTER_JOIN,
	'IS NOT NULL': EnumValueId.IS_NOT_NULL,	
	# Not Keyword
	'WITHIN': EnumValueId.WITHIN,
	'APPLY': EnumValueId.APPLY,
	'TRY': EnumValueId.TRY,
	'CATCH': EnumValueId.CATCH,
	'PARTITION': EnumValueId.PARTITION,
	'ROWS': EnumValueId.ROWS,
	'ROW': EnumValueId.ROW,
	'RANGE': EnumValueId.RANGE,
	'UNBOUNDED': EnumValueId.UNBOUNDED,
	'PRECEDING': EnumValueId.PRECEDING,
	'FOLLOWING': EnumValueId.FOLLOWING,
	'PATH': EnumValueId.PATH,
	'AUTO': EnumValueId.AUTO,
	'JSON': EnumValueId.JSON,
	'EXPLICIT': EnumValueId.EXPLICIT,
	'RAW': EnumValueId.RAW,
	'XML': EnumValueId.XML,
	'ABSENT': EnumValueId.ABSENT,
	'XSINIL': EnumValueId.XSINIL,
	'ELEMENTS': EnumValueId.ELEMENTS,
	'XMLSCHEMA': EnumValueId.XMLSCHEMA,
	'XMLDATA': EnumValueId.XMLDATA,
	'ROOT': EnumValueId.ROOT,
	'INCLUDE_NULL_VALUES': EnumValueId.INCLUDE_NULL_VALUES,
	'WITHOUT_ARRAY_WRAPPER': EnumValueId.WITHOUT_ARRAY_WRAPPER,
	'OPENJSON': EnumValueId.OPENJSON,
	'BINARY': EnumValueId.BINARY,
	'BASE64': EnumValueId.BASE64,
	'TYPE': EnumValueId.TYPE,
	'OFFSET': EnumValueId.OFFSET,
	'ONLY': EnumValueId.ONLY,
	'TIES': EnumValueId.TIES,
	'CAST': EnumValueId.CAST,
	'AVG': EnumValueId.AVG,
	'COUNT': EnumValueId.COUNT,
	'SUM': EnumValueId.SUM,
	'MIN': EnumValueId.MIN,
	'MAX': EnumValueId.MAX,
	'TINYINT': EnumValueId.TINYINT,
	'SMALLINT': EnumValueId.SMALLINT,
	'INT': EnumValueId.INT,
	'BIGINT': EnumValueId.BIGINT,
	'BIT': EnumValueId.BIT,
	'DECIMAL': EnumValueId.DECIMAL,
	'NUMERIC': EnumValueId.NUMERIC,
	'MONEY': EnumValueId.MONEY,
	'SMALLMONEY': EnumValueId.SMALLMONEY,
	'FLOAT': EnumValueId.FLOAT,
	'REAL': EnumValueId.REAL,
	'DATE': EnumValueId.DATE,
	'TIME': EnumValueId.TIME,
	'DATETIME2': EnumValueId.DATETIME2,
	'DATETIMEOFFSET': EnumValueId.DATETIMEOFFSET,
	'DATETIME': EnumValueId.DATETIME,
	'SMALLDATETIME': EnumValueId.SMALLDATETIME,
	'CHAR': EnumValueId.CHAR,
	'VARCHAR': EnumValueId.VARCHAR,
	'TEXT': EnumValueId.TEXT,
	'NCHAR': EnumValueId.NCHAR,
	'NVARCHAR': EnumValueId.NVARCHAR,
	'NTEXT': EnumValueId.NTEXT,
	'VARBINARY': EnumValueId.VARBINARY,
	'IMAGE': EnumValueId.IMAGE,
	'CURSOR': EnumValueId.CURSOR,
	'GEOGRAPHY': EnumValueId.GEOGRAPHY,
	'GEOMETRY': EnumValueId.GEOMETRY,
	'HIERARCHYID': EnumValueId.HIERARCHYID,
	'VECTOR': EnumValueId.VECTOR,
	'ROWVERSION': EnumValueId.ROWVERSION,
	'SQL_VARIANT': EnumValueId.SQL_VARIANT,
	'UNIQUEIDENTIFIER': EnumValueId.UNIQUEIDENTIFIER,
	'XML': EnumValueId.XML,
	# Delimiters
	'.': EnumValueId.DOT,
	',': EnumValueId.COMMA,
	';': EnumValueId.SEMICOLON,
	'(': EnumValueId.PARENTH_1,
	')': EnumValueId.PARENTH_2,
	# Operators
	'+': EnumValueId.OP_ADD,
	'-': EnumValueId.OP_SUB, 
	'*': EnumValueId.OP_MUL,
	'/': EnumValueId.OP_DIV,
	'%': EnumValueId.OP_MOD,
	'>': EnumValueId.GT,
	'<': EnumValueId.LT,
	'=': EnumValueId.EQ,
	'&': EnumValueId.BW_AND,
	'|': EnumValueId.BW_OR,
	'^': EnumValueId.BW_XOR,
	'~': EnumValueId.BW_NOT,
	'<>': EnumValueId.NE,
	'>=': EnumValueId.GE,
	'<=': EnumValueId.LE,
}

_KEYWORDS_1 = frozenset({
    EnumValueId.SESSION_USER,
    EnumValueId.VIEW,
    EnumValueId.NOT,
    EnumValueId.TSEQUAL,
    EnumValueId.SECURITYAUDIT,
    EnumValueId.CONVERT,
    EnumValueId.BROWSE,
    EnumValueId.UNPIVOT,
    EnumValueId.ROWCOUNT,
    EnumValueId.RETURN,
    EnumValueId.SEMANTICSIMILARITYDETAILSTABLE,
    EnumValueId.PROCEDURE,
    EnumValueId.DENY,
    EnumValueId.PIVOT,
    EnumValueId.AND,
    EnumValueId.TOP,
    EnumValueId.INTO,
    EnumValueId.SET,
    EnumValueId.END,
    EnumValueId.CASE,
    EnumValueId.CHECK,
    EnumValueId.COLUMN,
    EnumValueId.EXECUTE,
    EnumValueId.DISK,
    EnumValueId.MERGE,
    EnumValueId.INNER,
    EnumValueId.NATIONAL,
    EnumValueId.ERRLVL,
    EnumValueId.TEXTSIZE,
    EnumValueId.DROP,
    EnumValueId.USER,
    EnumValueId.DBCC,
    EnumValueId.AS,
    EnumValueId.HAVING,
    EnumValueId.BACKUP,
    EnumValueId.WHEN,
    EnumValueId.CURRENT_TIME,
    EnumValueId.OPTION,
    EnumValueId.SHUTDOWN,
    EnumValueId.CLOSE,
    EnumValueId.IDENTITY,
    EnumValueId.IS,
    EnumValueId.NOCHECK,
    EnumValueId.PRECISION,
    EnumValueId.FOR,
    EnumValueId.PUBLIC,
    EnumValueId.OR,
    EnumValueId.THEN,
    EnumValueId.FREETEXT,
    EnumValueId.CURSOR,
    EnumValueId.REFERENCES,
    EnumValueId.DECLARE,
    EnumValueId.CURRENT_DATE,
    EnumValueId.FREETEXTTABLE,
    EnumValueId.CROSS,
    EnumValueId.TRIGGER,
    EnumValueId.CURRENT,
    EnumValueId.BETWEEN,
    EnumValueId.LIKE,
    EnumValueId.EXEC,
    EnumValueId.GOTO,
    EnumValueId.CONTINUE,
    EnumValueId.ESCAPE,
    EnumValueId.NULLIF,
    EnumValueId.NONCLUSTERED,
    EnumValueId.FILE,
    EnumValueId.ON,
    EnumValueId.RECONFIGURE,
    EnumValueId.COMMIT,
    EnumValueId.COLLATE,
    EnumValueId.OVER,
    EnumValueId.SEMANTICSIMILARITYTABLE,
    EnumValueId.FETCH,
    EnumValueId.SEMANTICKEYPHRASETABLE,
    EnumValueId.TABLESAMPLE,
    EnumValueId.FILLFACTOR,
    EnumValueId.DATABASE,
    EnumValueId.DELETE,
    EnumValueId.OPENDATASOURCE,
    EnumValueId.RESTORE,
    EnumValueId.IDENTITY_INSERT,
    EnumValueId.KILL,
    EnumValueId.INTERSECT,
    EnumValueId.GRANT,
    EnumValueId.CONTAINSTABLE,
    EnumValueId.FROM,
    EnumValueId.VALUES,
    EnumValueId.TRY_CONVERT,
    EnumValueId.EXIT,
    EnumValueId.DOUBLE,
    EnumValueId.CURRENT_TIMESTAMP,
    EnumValueId.PROC,
    EnumValueId.EXCEPT,
    EnumValueId.HOLDLOCK,
    EnumValueId.WHERE,
    EnumValueId.PLAN,
    EnumValueId.TABLE,
    EnumValueId.CONTAINS,
    EnumValueId.REVOKE,
    EnumValueId.REPLICATION,
    EnumValueId.ASC,
    EnumValueId.TRUNCATE,
    EnumValueId.IN,
    EnumValueId.ADD,
    EnumValueId.READTEXT,
    EnumValueId.REVERT,
    EnumValueId.COALESCE,
    EnumValueId.USE,
    EnumValueId.CURRENT_USER,
    EnumValueId.OPENQUERY,
    EnumValueId.LOAD,
    EnumValueId.OF,
    EnumValueId.DUMP,
    EnumValueId.LINENO,
    EnumValueId.EXISTS,
    EnumValueId.OFF,
    EnumValueId.UNION,
    EnumValueId.DISTRIBUTED,
    EnumValueId.VARYING,
    EnumValueId.DESC,
    EnumValueId.SYSTEM_USER,
    EnumValueId.IF,
    EnumValueId.ELSE,
    EnumValueId.OPENXML,
    EnumValueId.SETUSER,
    EnumValueId.CLUSTERED,
    EnumValueId.WHILE,
    EnumValueId.WITH,
    EnumValueId.LEFT,
    EnumValueId.ROLLBACK,
    EnumValueId.WAITFOR,
    EnumValueId.SCHEMA,
    EnumValueId.DISTINCT,
    EnumValueId.BULK,
    EnumValueId.FUNCTION,
    EnumValueId.SAVE,
    EnumValueId.CONSTRAINT,
    EnumValueId.UPDATETEXT,
    EnumValueId.CASCADE,
    EnumValueId.FOREIGN,
    EnumValueId.OPEN,
    EnumValueId.ALL,
    EnumValueId.BREAK,
    EnumValueId.ROWGUIDCOL,
    EnumValueId.TRANSACTION,
    EnumValueId.UPDATE,
    EnumValueId.ANY,
    EnumValueId.BY,
    EnumValueId.ORDER,
    EnumValueId.EXTERNAL,
    EnumValueId.KEY,
    EnumValueId.TRAN,
    EnumValueId.OFFSETS,
    EnumValueId.RAISERROR,
    EnumValueId.SELECT,
    EnumValueId.CREATE,
    EnumValueId.GROUP,
    EnumValueId.FULL,
    EnumValueId.ALTER,
    EnumValueId.READ,
    EnumValueId.INSERT,
    EnumValueId.BEGIN,
    EnumValueId.STATISTICS,
    EnumValueId.OUTER,
    EnumValueId.OPENROWSET,
    EnumValueId.SOME,
    EnumValueId.RULE,
    EnumValueId.AUTHORIZATION,
    EnumValueId.PRINT,
    EnumValueId.DEALLOCATE,
    EnumValueId.PERCENT,
    EnumValueId.RIGHT,
    EnumValueId.INDEX,
    EnumValueId.JOIN,
    EnumValueId.PRIMARY,
    EnumValueId.UNIQUE,
    EnumValueId.WRITETEXT,
    EnumValueId.COMPUTE,
    EnumValueId.RESTRICT,
    EnumValueId.TO,
    EnumValueId.DEFAULT,
    EnumValueId.NULL,
    EnumValueId.CHECKPOINT,
    EnumValueId.IDENTITYCOL,
})

_KEYWORDS_2 = {
    (EnumValueId.INNER, EnumValueId.JOIN): ['INNER JOIN', EnumValueId.INNER_JOIN],
    (EnumValueId.CROSS, EnumValueId.JOIN): ['CROSS JOIN', EnumValueId.CROSS_JOIN],
    (EnumValueId.COMMIT, EnumValueId.TRAN): ['COMMIT TRAN', EnumValueId.COMMIT_TRAN],
    (EnumValueId.ADD, EnumValueId.CONSTRAINT): ['ADD CONSTRAINT', EnumValueId.ADD_CONSTRAINT],
    (EnumValueId.WITHIN, EnumValueId.GROUP): ['WITHIN GROUP', EnumValueId.WITHIN_GROUP],
    (EnumValueId.BEGIN, EnumValueId.TRAN): ['BEGIN TRAN', EnumValueId.BEGIN_TRAN],
    (EnumValueId.CROSS, EnumValueId.APPLY): ['CROSS APPLY', EnumValueId.CROSS_APPLY],
    (EnumValueId.BEGIN, EnumValueId.TRANSACTION): ['BEGIN TRANSACTION', EnumValueId.BEGIN_TRANSACTION],
    (EnumValueId.ROLLBACK, EnumValueId.TRANSACTION): ['ROLLBACK TRANSACTION', EnumValueId.ROLLBACK_TRANSACTION],
    (EnumValueId.BEGIN, EnumValueId.TRY): ['BEGIN TRY', EnumValueId.BEGIN_TRY],
    (EnumValueId.GROUP, EnumValueId.BY): ['GROUP BY', EnumValueId.GROUP_BY],
    (EnumValueId.END, EnumValueId.CATCH): ['END CATCH', EnumValueId.END_CATCH],
    (EnumValueId.FULL, EnumValueId.JOIN): ['FULL JOIN', EnumValueId.FULL_JOIN],
    (EnumValueId.COMMIT, EnumValueId.TRANSACTION): ['COMMIT TRANSACTION', EnumValueId.COMMIT_TRANSACTION],
    (EnumValueId.ADD, EnumValueId.COLUMN): ['ADD COLUMN', EnumValueId.ADD_COLUMN],
    (EnumValueId.BEGIN, EnumValueId.CATCH): ['BEGIN CATCH', EnumValueId.BEGIN_CATCH],
    (EnumValueId.LEFT, EnumValueId.JOIN): ['LEFT JOIN', EnumValueId.LEFT_JOIN],
    (EnumValueId.ROLLBACK, EnumValueId.TRAN): ['ROLLBACK TRAN', EnumValueId.ROLLBACK_TRAN],
    (EnumValueId.ORDER, EnumValueId.BY): ['ORDER BY', EnumValueId.ORDER_BY],
    (EnumValueId.END, EnumValueId.TRY): ['END TRY', EnumValueId.END_TRY],
    (EnumValueId.RIGHT, EnumValueId.JOIN): ['RIGHT JOIN', EnumValueId.RIGHT_JOIN],
    (EnumValueId.OUTER, EnumValueId.APPLY): ['OUTER APPLY', EnumValueId.OUTER_APPLY],
    (EnumValueId.IS, EnumValueId.NULL): ['IS NULL', EnumValueId.IS_NULL],
    (EnumValueId.NOT, EnumValueId.IN): ['NOT IN', EnumValueId.NOT_IN],
    (EnumValueId.NOT, EnumValueId.BETWEEN): ['NOT BETWEEN', EnumValueId.NOT_BETWEEN],
    (EnumValueId.NOT, EnumValueId.LIKE): ['NOT LIKE', EnumValueId.NOT_LIKE],
    (EnumValueId.NOT, EnumValueId.EXISTS): ['NOT EXISTS', EnumValueId.NOT_EXISTS],
}
_KEYWORDS_3 = {
    (EnumValueId.RIGHT, EnumValueId.OUTER, EnumValueId.JOIN): ['RIGHT OUTER JOIN', EnumValueId.RIGHT_OUTER_JOIN],
    (EnumValueId.LEFT, EnumValueId.OUTER, EnumValueId.JOIN): ['LEFT OUTER JOIN', EnumValueId.LEFT_OUTER_JOIN],
    (EnumValueId.FULL, EnumValueId.OUTER, EnumValueId.JOIN): ['FULL OUTER JOIN', EnumValueId.FULL_OUTER_JOIN],
    (EnumValueId.IS, EnumValueId.NOT, EnumValueId.NULL): ['IS NOT NULL', EnumValueId.IS_NOT_NULL],
}

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

def find_token_at(self, tokens: List[Token], position: int) -> Token | None:
	"""
	Find the token that covers a given character position.

	Args:
		tokens (List[TSqlToken]): List of tokens to search.
		position (int): Character index within the SQL script.

	Returns:
		TSqlToken | None: The token that contains the position, or None if not found.
	"""
	return next((t for t in tokens if t.start <= position < t.end), None)

def _flush_buffer(buf: list[Token]) -> Iterator[Token]:

	# Compound Keywords
	i=0
	while i < len(buf):
		pending = len(buf) - i
		if pending >=3 and (val := _KEYWORDS_3.get((buf[i].value_id, buf[i+1].value_id, buf[i+2].value_id))) != None:
			buf[i].value = val[0]
			buf[i].end = buf[i+2].end
			buf[i].type = EnumTokenType.KEYWORD
			buf[i].value_id = val[1]
			del buf[i+1:i+3]
		elif pending >= 2 and (val := _KEYWORDS_2.get((buf[i].value_id, buf[i+1].value_id))) != None:
			buf[i].value = val[0]
			buf[i].end = buf[i+1].end
			buf[i].type = EnumTokenType.KEYWORD
			buf[i].value_id = val[1]
			del buf[i+1:i+2]
		elif buf[i].value_id in _KEYWORDS_1:
			buf[i].type = EnumTokenType.KEYWORD

		i += 1

	while buf:
		# Merge dotted identifiers
		if buf[0].type == EnumTokenType.IDENTIFIER.value:
			while len(buf) >= 3 and buf[1].value == '.' and buf[2].type != EnumTokenType.KEYWORD.value:
				buf[0].value += '.' + buf[2].value
				buf[0].end = buf[2].end
				del buf[1:3]

		yield buf.pop(0)

def lex(sql, quoted_identifiers = True) -> Iterator[Token]:
	if quoted_identifiers: is_identifier = lambda value:(value[0] == '[' or value[0] == '"')
	else: is_identifier = lambda value:(value[0] == '[')

	it = tokenize(text=sql,
					word_start=frozenset('_@#' + string.ascii_letters),
					word_chars=frozenset('_@#$' + string.ascii_letters + string.digits),
					delimited_constructs={"'": "'", '"': '"', '[': "]"},
					line_comment='--',
					block_comments=['/*', '*/'],
					operators1char=frozenset('><=-+*/%&|^~'),
					operators2chars=frozenset(['<>', '<=', '>=']),
					is_identifier=is_identifier,
					value_hash=value_hash,
					comments=False
					)
	
	buf:list[Token] = []
	for t in it:
		if t.value_id == EnumValueId.DOT or (t.type == EnumTokenType.IDENTIFIER and t.value[0] not in('@', '#')):
			buf.append(t)
			continue
		yield from _flush_buffer(buf)
		yield t
	yield from _flush_buffer(buf=buf)
