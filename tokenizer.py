from dataclasses import dataclass
from typing import Iterator
import string
from enum import IntEnum

class EnumTokenType(IntEnum):
	IDENTIFIER = 1
	INTEGER = 2
	DECIMAL = 3
	DELIMITED_LITERAL = 4
	OPERATOR = 5
	DELIMITER = 6
	LINE_COMMENT = 7
	BLOCK_COMMENT = 8
	KEYWORD = 9

@dataclass
class Token:
	start: int
	end: int
	type:int # 1 word, 2 number, 3 delimited_literal, 4 operator, 5 delimiter
	value:str
	value_id: int=None

	def get_value(self, sql):
		return sql[self.start : self.end]
	def get_position(self, sql: str) -> tuple[int, int]:
		"""Get line number and column"""
		lines = sql[:self.start].split('\n')
		return len(lines), len(lines[-1]) + 1

def tokenize(
	text: str,
	word_start=frozenset('_@#' + string.ascii_letters),
	word_chars=frozenset('_@#$' + string.ascii_letters + string.digits),
	delimited_constructs={"'": "'", '"': '"', '[': "]"},
	line_comment='--',
	block_comments=['/*', '*/'],
	operators1char=frozenset('><=-+*/%&|^~'),
	operators2chars=frozenset(['<>', '<=', '>=']),
	is_identifier = None,
	value_hash={},
	comments = False
) -> Iterator[Token]:
	
	text, i, n, linecomment_len = text + '\n', 0, len(text) + 1, len(line_comment)

	block_opening, block_closing = block_comments[0], block_comments[1]
	opening_len, closing_len = len(block_opening), len(block_closing)

	while i < n:
		if text[i].isspace(): i += 1; continue
		start, c = i, text[i]

		# Identifier
		if c in word_start:
			while i < n and text[i] in word_chars: i += 1
			value = text[start:i].upper()
			yield Token(start, i, type=EnumTokenType.IDENTIFIER, value=value, value_id=value_hash.get(value)); continue

		# Number
		dot = False
		if c == '.' and text[i+1:i+2].isdigit():
			dot = True
			i += 1
		while i < n and text[i].isdigit(): i += 1
		if start != i:
			if text[i] == '.' and dot == False:
				i += 1
				while i < n and text[i].isdigit(): i += 1

			if text[i] not in('E','e'):
				yield Token(start, i, type=EnumTokenType.INTEGER if dot==False else EnumTokenType.DECIMAL, value=text[start:i])
			else:
				i += 1
				if text[i] in ('+', '-'):
					i += 1
				while i < n and text[i].isdigit(): i += 1
				yield Token(start, i, type=EnumTokenType.INTEGER if dot==False else EnumTokenType.DECIMAL, value=text[start:i])
			continue

		# Line comment
		if text[i:i+linecomment_len] == line_comment:
			start = i
			i = text.find('\n', i+2) + 1 or n; 
			if comments:
				yield Token(start, i, type=EnumTokenType.LINE_COMMENT, value=text[start:i])
			continue

		# Block comment
		if text[i:i+opening_len] == block_opening:
			start = i
			depth, i = 1, i + opening_len
			while i < n and depth:
				if text[i:i+opening_len] == block_opening: depth += 1; i += opening_len
				elif text[i:i+closing_len] == block_closing: depth -= 1; i += closing_len
				else: i += 1
			if comments:
				yield Token(start, i, type=EnumTokenType.BLOCK_COMMENT, value=text[start:i])
			continue

		# Delimited literal
		if c in delimited_constructs:
			literal_closing, i = delimited_constructs[c], i+1
			while i < n:
				if text[i] == literal_closing and text[i+1:i+2] != literal_closing: i += 1; break
				i += 2 if text[i:i+2] == literal_closing*2 else 1
			value = text[start:i]
			value_id = None
			if is_identifier != None and is_identifier(value): 
				ty = EnumTokenType.IDENTIFIER
				value_id = value_hash.get(value)
			else: ty = EnumTokenType.DELIMITED_LITERAL
			yield Token(start, i, type=ty, value=value, value_id=value_id)
			continue

		# Operator / delimiter
		if text[i:i+2] in operators2chars:
			value = text[i:i+2]
			yield Token(i, i+2, type=EnumTokenType.OPERATOR, value=value, value_id=value_hash.get(value)); i += 2
		elif c in operators1char:
			value = text[i:i+1]
			yield Token(i, i+1, type=EnumTokenType.OPERATOR, value=value, value_id=value_hash.get(value)); i += 1
		else:
			value = text[i:i+1]
			yield Token(i, i+1, type=EnumTokenType.DELIMITER, value=value, value_id=value_hash.get(value)); i += 1
