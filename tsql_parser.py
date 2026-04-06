from tsql_lexer import lex, EnumValueId as I, EnumTokenType as Ty
from enum import IntEnum, auto

class Tok:
    SQL, TOKENS, LEN, idx, i, t = "", [], 0, 0, None, None
    @staticmethod
    def init(sql): 
        Tok.SQL, Tok.TOKENS = sql, list(lex(sql))
        Tok.LEN = len(Tok.TOKENS)
        Tok.seek(0)
    @staticmethod
    def consume_one():
        Tok.seek(Tok.idx + 1)
        return Tok.idx - 1
    @staticmethod
    def seek(idx):
        Tok.idx = idx
        if Tok.idx < Tok.LEN:
            Tok.i = Tok.TOKENS[Tok.idx].value_id
            Tok.t = Tok.TOKENS[Tok.idx].type
        else:
            Tok.i = None
            Tok.t = None

class N(IntEnum):
    row_range = auto()
    frame_bount = auto()
    over = auto()
    data_type = auto()
    function_call = auto()
    primary_expression = auto()
    collate = auto()
    expression = auto()
    condition = auto()
    not_condition = auto()
    exists_condition = auto()
    binary_condition = auto()
    null_condition = auto()
    between_condition = auto()
    in_condition = auto()
    logical_expression = auto()
    case_expresion = auto()
    select_column = auto()
    list_of = auto()
    alias = auto()
    rowset_function = auto()
    schema_column_declaration = auto()
    openxml = auto()
    openjson = auto()
    tuple = auto()
    derived_table = auto()
    table_value_constructor = auto()
    column_list = auto()
    pivot_clause = auto()
    unpivot_clause = auto()
    table_or_view_name = auto()
    user_defined_function = auto()
    table_source = auto()
    pivoted_table = auto()
    unpivoted_table = auto()
    select_clause = auto()
    from_clause = auto()
    where_clause = auto()
    group_by_clause = auto()
    having_clause = auto()
    order_by_clause = auto()
    for_cluase = auto()
    common_directives = auto()
    elements = auto()
    raw_auto_directives = auto()
    top_clause = auto()
    frame_bound = auto()
    select_statemet = auto()
    value_expression_list = auto()
    primitive_value_list = auto()
    schema_column_list = auto()
    tuple_list = auto()
    table_source_list = auto()
    argument_list = auto()
    for_directive_name = auto()

class Node(list):
    def __init__(self, type:str):
        self.type = type
        
def walk(node, parents=[]):
    l = []
    for item in node:
        if isinstance(item, Node): 
            l += walk(item, parents+[item])
        elif isinstance(item, int): 
            l += [(parents , Tok.TOKENS[item])]
        else: 
            raise Exception(f'Invalid node {type(item)} at {"/".join([t.type.name for t in parents])}')
    return l

def error(m=""):
    t = Tok.TOKENS[Tok.idx] if Tok.idx < Tok.LEN else Tok.TOKENS[-1]
    line, col = t.get_position(Tok.SQL)
    raise Exception(f'Error in "{t.value}" (L{line}:C{col}) idx {Tok.idx} {m}')

def matchi(i, off):
    if 0 <= Tok.idx+off < Tok.LEN:
        if (t:=Tok.TOKENS[Tok.idx+off]):
            return t.value_id == i
    return False

def matchxi(*i, off=1):
    if 0 <= Tok.idx+off < Tok.LEN:
        if (t:=Tok.TOKENS[Tok.idx+off]):
            return t.value_id in i
    return False

def inspect(off=0):
    return Tok.TOKENS[Tok.idx+off] if 0 <= Tok.idx+off < Tok.LEN else None

def _tok():
    if Tok.idx >= Tok.LEN:
        error('Unexpected EOF.')
    return Tok.consume_one()

def _itok(exp:I):
    if Tok.idx >= Tok.LEN:
        error('Unexpected EOF.')
    elif Tok.i != exp:
        error(f"{exp.name} expected.")
    return Tok.consume_one()

def _xitok(*exp):
    if Tok.idx >= Tok.LEN:
        error('Unexpected EOF.')
    elif Tok.i not in exp:
        error(f"{'|'.join([e.name for e in exp])} expedted.")
    return Tok.consume_one()

def _ttok(exp):
    if Tok.idx >= Tok.LEN:
        error('Unexpected EOF.')
    elif Tok.t != exp:
        error(f"{exp.name} expected.")
    return Tok.consume_one()

def _xttok(*exp):
    if Tok.idx >= Tok.LEN:
        error('Unexpected EOF.')
    elif Tok.t not in exp:
        error(f"{'|'.join([e.name for e in exp])} expeted.")
    return Tok.consume_one()

############################################################################################

def _frame_bound(type):
    if (Tok.i == I.UNBOUNDED and matchi(type, off=1)) \
    or (Tok.i == I.CURRENT and matchi(I.ROW, off=1)) \
    or (Tok.t == Ty.INTEGER and matchi(type, off=1)):
        n = Node(N.frame_bound)
        n+=[_tok(), _tok()]
        return n
    error("Frame bound expected.")

def _row_range():
    n = Node(N.row_range)
    n.append(_tok()) # ROWS or RANGE
    if Tok.i == I.BETWEEN:
        n+=[_tok(), _frame_bound(I.PRECEDING), _itok(I.AND), _frame_bound(I.FOLLOWING)]
    else:
        n.append(_frame_bound(I.PRECEDING))
    return n

def _over():
    n = Node(N.over)
    n += [_itok(I.OVER), _itok(I.PARENTH_1)]
    if Tok.i == I.PARTITION and matchi(I.BY, off=1): n += [_tok(), _tok(), _list(_expression, N.value_expression_list)]
    if Tok.i == I.ORDER_BY: n.append(_order_by())
    if Tok.i in (I.ROWS, I.RANGE): n.append(_row_range())
    n.append(_itok(I.PARENTH_2))
    return n

def _datatype():
    n = Node(N.data_type)
    match Tok.i:
        case I.CHAR | I.VARCHAR | I.NCHAR | I.NVARCHAR | I.DATETIMEOFFSET | I.DATETIME2:
            n.append(_tok())
            if Tok.i == I.PARENTH_1: n +=[_tok(), _ttok(Ty.INTEGER), _itok(I.PARENTH_2)]
        case I.DECIMAL | I.NUMERIC:
            n.append(_tok())
            if Tok.i == I.PARENTH_1:
                n +=[_tok(), _ttok(Ty.INTEGER)]
                if Tok.i == I.COMMA: n += [_tok(), _ttok(Ty. INTEGER)]
                n.append(_itok(I.PARENTH_2))
        case I.TINYINT | I.SMALLINT | I.INT | I.BIGINT | I.BIT | \
             I.DECIMAL | I.NUMERIC | I.MONEY | I.SMALLMONEY | I.FLOAT | I.REAL | I.MONEY | I.SMALLMONEY | \
             I.DATE | I.TIME | I.DATETIME | \
             I.TEXT | I.NTEXT | I.VARBINARY | \
             I.IMAGE | I.GEOGRAPHY | I.GEOMETRY | I.HIERARCHYID | I.JSON | I.VECTOR | I.ROWVERSION | I.SQL_VARIANT | \
             I.UNIQUEIDENTIFIER | I.XML:
            n.append(_tok())
        case _:
            error('Data type expected.')
    return n

def _function_call():
    n = Node(N.function_call)
    distinct = False
    if Tok.i == I.CAST:
        n +=[_tok(), _itok(I.PARENTH_1), _expression(), _itok(I.AS), _datatype(), _itok(I.PARENTH_2)]
    elif matchi(I.DISTINCT, off=2):
        distinct = True
        n +=[_ttok(Ty.IDENTIFIER), _itok(I.PARENTH_1), _itok(I.DISTINCT), _list(_primary_expression, N.primitive_value_list), _itok(I.PARENTH_2)]
    else:
        n +=[_ttok(Ty.IDENTIFIER), _itok(I.PARENTH_1), _list(_primary_expression, N.primitive_value_list), _itok(I.PARENTH_2)]

    if Tok.i == I.OVER:
        if distinct:
            error("Unexpected DISTINCT.")
        n.append(_over())
    return n

def _collate():
    n = Node(N.collate)
    n +=[_tok(), _ttok(Ty.IDENTIFIER)]
    return n

def _primary_expression():
    p = Node(N.primary_expression)
    while Tok.i in(I.OP_ADD, I.OP_SUB): p.append(_tok())
    if Tok.i == I.CASE: 
         p+=_case()
         return p
    elif Tok.i == I.PARENTH_1:
        if matchxi(I.SELECT, I.INSERT, I.UPDATE, I.DELETE, off=1):
            p+=[_itok(I.PARENTH_1), _select(), _itok(I.PARENTH_2)]
            return p
        else:
            p+=[_itok(I.PARENTH_1), _expression(), _itok(I.PARENTH_2)]
            return p
    elif Tok.t in (Ty.INTEGER, Ty.DECIMAL, Ty.DELIMITED_LITERAL):
        p+=[_tok()]
        return p
    elif Tok.i in(I.CURRENT_DATE, I.CURRENT_TIME, I.CURRENT_TIMESTAMP, I.CURRENT_USER):
        p+=[_tok()]
        return p
    elif Tok.t == Ty.IDENTIFIER:
        if matchi(I.PARENTH_1, off=1):
            p+=_function_call()
            return p
        p+=[_tok()]
        return p
    error('Value or expression expected.')

def _expression():
    n = Node(N.expression)
    n.append(_primary_expression())
    while Tok.i in(I.OP_ADD, I.OP_SUB, I.OP_MUL, I.OP_DIV, I.OP_MOD):
        n += [_tok(), _primary_expression()]
    if Tok.i == I.COLLATE:
        n.append(_collate())
    return n

def _primary_condition():
    # Without left expression
    match Tok.i:
        case I.NOT:
            n = Node(N.not_condition)
            n += [_tok(), _primary_condition()]
            return n
        case I.EXISTS | I.NOT_EXISTS:
            n = Node(N.exists_condition) 
            n += [_tok(), _itok(I.PARENTH_1), _select(), _itok(I.PARENTH_2)]
            return n
        case I.PARENTH_1:
            if not matchxi(I.SELECT, I.INSERT, I.UPDATE, I.DELETE, off=1):
                start_idx = Tok.idx
                try:
                    n = Node(N.condition)
                    n += [_itok(I.PARENTH_1), _condition(), _itok(I.PARENTH_2)]
                    return n
                except: pass
                # Backtrack
                Tok.seek(start_idx)
    
    # With left expression
    left_expr = _expression()
    match Tok.i:
        case I.EQ | I.NE | I.GE | I.LE | I.LT | I.GT | I.LIKE | I.NOT_LIKE: 
            n = Node(N.binary_condition)
            n += [left_expr, _tok(), _expression()]
            return n
        case I.IS_NULL | I.IS_NOT_NULL:
            n = Node(N.null_condition)
            n += [left_expr, _tok()]
            return n
        case I.BETWEEN | I.NOT_BETWEEN:
            n = Node(N.between_condition)
            n += [left_expr, _tok(), _expression(), _itok(I.AND), _expression()]
            return n
        case I.IN | I.NOT_IN:
            cond = Node(N.in_condition)
            op = _tok()
            if matchxi(I.SELECT, I.INSERT, I.UPDATE, I.DELETE, off=1):
                cond += [left_expr, op, _itok(I.PARENTH_1), _select(), _itok(I.PARENTH_2)]
            else:
                cond += [left_expr, op, _itok(I.PARENTH_1), _list(_expression, N.value_expression_list), _itok(I.PARENTH_2)]
            return cond
    
    error('Logical operator expected.')

def _condition():
    n = Node(N.condition)
    n.append(_primary_condition())
    while Tok.i in(I.AND, I.OR):
        n += [_tok(), _primary_condition()]
    return n[0] if len(n) == 1 else  n

def _case():
    n = Node(N.case_expresion)
    n.append(_itok(I.CASE))
    if Tok.i == I.WHEN: 
        fn = _condition  
    else:
        n.append(_expression())
        fn = _expression
    while Tok.i == I.WHEN: n += [_itok(I.WHEN), fn(), _itok(I.THEN), _expression()]
    if Tok.i == I.ELSE: n += [_itok(I.ELSE), _expression()]
    n += [_itok(I.END)]
    return n

def _select_column():
    n = Node(N.select_column)
    if Tok.i == I.OP_MUL: # Tok.i == '*'
        n.append(_tok())
    elif Tok.t == Ty.IDENTIFIER and matchi(I.EQ, off=1): # Case: alias = expr
        n += [_tok(), _tok()]
        n.append(_expression())
    else:
        n.append(_expression())
        if (a:=_if_alias()): n.append(a)
    return n

def _list(fn, node_type:N):
    n = Node(node_type)
    n.append(fn())
    sep=I.COMMA
    while Tok.i == sep: n += [_tok(), fn()]
    return n

def _if_alias():
    n = Node(N.alias)
    if Tok.i == I.AS: n+=[_tok(), _ttok(Ty.IDENTIFIER)]; return n
    elif Tok.t == Ty.IDENTIFIER: n.append(_tok()); return n
    else: return None

def _rowset_function():
    n = Node(N.rowset_function)
    match Tok.i:
        case I.OPENROWSET: n+=[_tok(), _itok(I.PARENTH_1), _ttok(Ty.DELIMITED_LITERAL), _itok(I.COMMA), _ttok(Ty.DELIMITED_LITERAL), _itok(I.COMMA), _ttok(Ty.DELIMITED_LITERAL), _itok(I.PARENTH_2)]
        case I.OPENQUERY: n+=[_tok(), _itok(I.PARENTH_1), _ttok(Ty.IDENTIFIER), _itok(I.COMMA), _ttok(Ty.DELIMITED_LITERAL), _itok(I.PARENTH_2)]
        case I.OPENDATASOURCE: n+=[_tok(), _itok(I.PARENTH_1), _ttok(Ty.DELIMITED_LITERAL), _itok(I.COMMA), _ttok(Ty.DELIMITED_LITERAL), _itok(I.PARENTH_2)]

    if a:=_if_alias(): n.append(a)
    return n

def _schema_column_declaration():
    n = Node(N.schema_column_declaration)
    n+=[_ttok(Ty.IDENTIFIER), _datatype()]
    return n

def _openxml():
    n = Node(N.openxml)
    n += [_tok(), _itok(I.PARENTH_1)]
    aux = inspect()
    if not aux or aux.value[0]!='@':
        error("Variable expected.")
    n+=[_tok(), _itok(I.COMMA), _ttok(Ty.DELIMITED_LITERAL)]
    if Tok.i == I.COMMA: n+=[_tok(), _ttok(Ty.INTEGER)]
    n+=[_itok(I.PARENTH_2), _itok(I.WITH), _itok(I.PARENTH_1)]
    if Tok.t != Ty.IDENTIFIER:
        error("Identifier expected.")
    elif matchi(I.PARENTH_2, off=1):
        n.append(_tok())
    else:
        n.append(_list(_schema_column_declaration, N.schema_column_list))
    n.append(_itok(I.PARENTH_2))
    if (a:=_if_alias()): n.append(a)
    return n

def _json_coldef():
    c = _schema_column_declaration()
    if Tok.t == Ty.DELIMITED_LITERAL: c.append(_tok())
    return c

def _openjson():
    n = Node(N.openjson)
    n += [_tok(), _itok(I.PARENTH_1), _xttok(Ty.IDENTIFIER, Ty.DELIMITED_LITERAL)]
    if Tok.i == I.COMMA: n+=[_tok(), _ttok(Ty.DELIMITED_LITERAL)]
    n.append(_itok(I.PARENTH_2))
    if Tok.i == I.WITH:
        n+=[_tok(), _itok(I.PARENTH_1), _list(_json_coldef, N.schema_column_list), _itok(I.PARENTH_2)]
    if (a:=_if_alias()): n.append(a)
    return n

def _tuple():
    n = Node(N.tuple)
    n += [_itok(I.PARENTH_1), _list(_expression, N.value_expression_list), _itok(I.PARENTH_2)]
    return n

def _derived_table():
    n = Node(N.derived_table)
    n+=[_tok(), _select(), _itok(I.PARENTH_2)]
    if (a:=_if_alias()): 
        n.append(a)
    else:
        error('Alias expected.')
    return n

def _table_value_construct():
    n = Node(N.table_value_constructor)
    n+=[_tok(), _tok(), _list(_tuple, N.tuple_list), _itok(I.PARENTH_2)]
    if (a:=_if_alias()): 
        n+=[a, _itok(I.PARENTH_1), _column_list(), _itok(I.PARENTH_2)]
    else:
        error('Alias expected')
    return n
    
def _column_list():
    n = Node(N.column_list)
    n.append(_ttok(Ty.IDENTIFIER))
    while Tok.i == I.COMMA:
        n += [_tok(), _ttok(Ty.IDENTIFIER)]
    return n

def _pivot_clause():
    n = Node(N.pivot_clause)
    n+=[_itok(I.PARENTH_1), _xitok(I.AVG, I.COUNT, I.SUM, I.MIN, I.MAX), _itok(I.PARENTH_1), _ttok(Ty.IDENTIFIER), _itok(I.PARENTH_2)
        , _itok(I.FOR), _ttok(Ty.IDENTIFIER), _itok(I.IN), _itok(I.PARENTH_1), _column_list(), _itok(I.PARENTH_2), _itok(I.PARENTH_2)]
    return n

def _unpivot_clause():
    n = Node(N.unpivot_clause)
    n+=[_itok(I.PARENTH_1), _ttok(Ty.IDENTIFIER), _itok(I.FOR), _ttok(Ty.IDENTIFIER), _itok(I.IN), _itok(I.PARENTH_1), _column_list(), _itok(I.PARENTH_2), _itok(I.PARENTH_2)]
    return n

def _table_or_view_name():
    n = Node(N.table_or_view_name)
    n.append(_tok())
    if(a:=_if_alias()):
        n.append(a)
    if Tok.i == I.WITH:
        n+=[_tok(), _itok(I.PARENTH_1), _ttok(Ty.IDENTIFIER), _itok(I.PARENTH_2)]
    return n

def _udf_table():
    n = Node(N.user_defined_function)
    n += [_tok(), _tok(), _list(_primary_expression, N.argument_list), _itok(I.PARENTH_2)]
    if(a:=_if_alias()): n.append(a)
    return n

def _table_source():
    left = Node(N.table_source)
    if Tok.i == I.OPENJSON: left = _openjson()
    elif Tok.i in(I.OPENROWSET, I.OPENQUERY, I.OPENDATASOURCE): left =_rowset_function()
    elif Tok.i == I.OPENXML: left = _openxml()
    elif Tok.t == Ty.IDENTIFIER and matchi(I.PARENTH_1, off=1): left =_udf_table()
    elif Tok.t == Ty.IDENTIFIER: left =_table_or_view_name()
    elif Tok.i == I.PARENTH_1 and matchxi(I.SELECT, I.INSERT, I.UPDATE, I.DELETE, off=1): left = _derived_table()
    elif Tok.i == I.PARENTH_1 and matchi(I.VALUES, off=1): left = _table_value_construct()
    elif Tok.i == I.PARENTH_1: left += [_tok(), _table_source(), _itok(I.PARENTH_2)]
    else: error("Table source expected.")

    while Tok.i in(I.JOIN, I.INNER_JOIN, I.LEFT_JOIN, I.RIGHT_JOIN, I.FULL_JOIN, I.LEFT_OUTER_JOIN, I.RIGHT_OUTER_JOIN, I.FULL_OUTER_JOIN, I.CROSS_JOIN, I.CROSS_APPLY, I.OUTER_APPLY, I.PIVOT,  I.UNPIVOT):
        match Tok.i:
            case I.PIVOT:
                n = Node(N.pivoted_table)
                n += [_tok(), _pivot_clause()]
                if a:=_if_alias(): n.append(a)
                left += n
            case I.UNPIVOT:
                n = Node(N.unpivoted_table)
                n += [_tok(), _unpivot_clause()]
                if a:=_if_alias(): n.append(a)
                left += n    
            case I.JOIN | I.INNER_JOIN | I.LEFT_JOIN | I.RIGHT_JOIN | I.FULL_JOIN | I.LEFT_OUTER_JOIN | I.RIGHT_OUTER_JOIN | I.FULL_OUTER_JOIN:
                left += [_tok(), _table_source(), _itok(I.ON), _condition()]
            case I.CROSS_JOIN | I.CROSS_APPLY | I.OUTER_APPLY:
                left += [_tok(), _table_source()]
        
    return left

def _from():
    n = Node(N.from_clause)
    n.append(_itok(I.FROM))
    n.extend(_list(_table_source, N.table_source_list))
    return n

def _where():
    n = Node(N.where_clause)
    n+=[_tok(), _condition()]
    return n

def _group_by():
    n = Node(N.group_by_clause)
    n+=[_tok(), _list(_expression, N.value_expression_list)]
    return n

def _having():
    n = Node(N.having_clause)
    n+=[_tok(), _condition()]
    return n

def _order_by():
    n = Node(N.order_by_clause)
    n+=[_tok(), _list(_expression, N.value_expression_list)]
    if Tok.i == I.OFFSET:
        n+=[_tok(), _expression(), _itok((I.ROW, I.ROWS))]
        if Tok.i == I.FETCH:
            n+=[_tok(), _expression(), _itok((I.ROW, I.ROWS)), _itok(I.ONLY)]
    return n

def _for_directive_name():
    n = Node(N.for_directive_name)
    n += [_itok(I.PARENTH_1), _ttok(Ty.DELIMITED_LITERAL), _itok(I.PARENTH_2)]
    return n

def _for_directive(words, name=False):
    if Tok.i == I.COMMA:
        for i, w in enumerate(words, 1):
            if matchi(w, off=i) == False:
                return
        ls = [_tok()]
        ls.extend([_tok() for t in range(len(words))])
        if name and Tok.i == I.PARENTH_1:
            ls.extend(_for_directive_name())
        return ls

def _for_common_directives():
    d=Node(N.common_directives)
    if (ls:=_for_directive([I.BINARY, I.BASE64])): d.extend(ls)
    if (ls:=_for_directive([I.TYPE])): d.extend(ls)
    if (ls:=_for_directive([I.ROOT], name=True)): d.extend(ls)
    return d
def _elements():
    e = Node(N.elements)
    if Tok.i == I.COMMA and matchi(I.ELEMENTS, off=1):
        e.append(_tok())
        e.append(_tok())
        match Tok.i:
            case I.XSINIL:
                e.append(_tok())
            case I.ABSENT:
                e.append(_tok())
    return e
def _raw_auto():
    ra=Node(N.raw_auto_directives)
    ra.append(_for_common_directives())
    if (ls:=_for_directive([I.XMLDATA])): ra.extend(ls)
    elif (ls:=_for_directive([I.XMLSCHEMA], name=True)): ra.extend(ls)
    ra.append(_elements())
    return ra

def _for():
    n = Node(N.for_cluase)
    n.append(_tok())
    match Tok.i:
        case I.BROWSE:
            n.append(_tok())
        case I.XML:
            n.append(_tok())
            match Tok.i:
                case I.RAW:
                    n.append(_tok())
                    if Tok.i == I.PARENTH_1: n.append(_for_directive_name())
                    n.append(_raw_auto())
                case I.AUTO:
                    n.append(_tok())
                    n.append(_raw_auto())
                case I.PATH: 
                    n.append(_tok())
                    if Tok.i == I.PARENTH_1: n.append(_for_directive_name())
                    n.append(_for_common_directives())
                    n.append(_elements())
                case I.EXPLICIT:
                    n.append(_tok())
                    n.append(_for_common_directives())
                    if (ls:=_for_directive([I.XMLDATA])): n.extend(ls)
                case _:
                    error("XML mode expected.")
        case I.JSON:
            n.append(_tok())
            match Tok.i:
                case I.AUTO: 
                    n.append(_tok())
                case I.PATH: 
                    n.append(_tok())
                    if Tok.i == I.PARENTH_1: n.append(_for_directive_name())
                case _:
                    error("JSON mode expected.")
            if (ls:=_for_directive([I.ROOT], name=True)): n.extend(ls)
            if (ls:=_for_directive([I.INCLUDE_NULL_VALUES])): n.extend(ls)
            if (ls:=_for_directive([I.WITHOUT_ARRAY_WRAPPER])): n.extend(ls)
        case _:
            error('BROWSE, XML or JSON expected.')
        
    return n

def _top():
    n = Node(N.top_clause)
    n+=[_itok(I.TOP), _primary_expression()]
    if Tok.i == I.PERCENT: n.append(_tok())
    if Tok.i == I.WITH and matchi(I.TIES, off=1):
        n+=[_tok(), _tok()]
    return n

def _select_clause():
    n = Node(N.select_clause)
    n.append(_itok(I.SELECT))
    if Tok.i in (I.ALL, I.DISTINCT):
        n.append(_tok())
    if Tok.i == I.TOP: n.append(_top())
    n.append(_list(_select_column, N.column_list))
    return n

def _select():
    n = Node(N.select_statemet)
    n.append(_select_clause())
    if Tok.i == I.INTO: n+=[_tok(), _ttok(Ty.IDENTIFIER)]
    if Tok.i == I.FROM: n.append(_from())
    if Tok.i == I.WHERE: n.append(_where())
    if Tok.i == I.GROUP_BY: n.append(_group_by())
    if Tok.i == I.HAVING: n.append(_having())
    if Tok.i == I.ORDER_BY: n.append(_order_by())
    if Tok.i == I.FOR:  n.append(_for())
    return n
