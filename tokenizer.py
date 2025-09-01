from dataclasses import dataclass
from typing import Iterator
import string
from enum import IntEnum

WORD = 1
NUMBER = 2
DELIMITED_LITERAL = 3
OPERATOR = 4
DELIMITER = 5
LINE_COMMENT = 6
BLOCK_COMMENT = 7

@dataclass
class Token:
	start: int
	end: int
	type:int # 1 word, 2 number, 3 delimited_literal, 4 operator, 5 delimiter

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
	operators2chars=frozenset(['<>', '<=', '>='])
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
			yield Token(start, i, type=WORD); continue

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

			if text[i] not in('E,e'):
				yield Token(start, i, type=2)
			else:
				i += 1
				if text[i] in ('+', '-'):
					i += 1
				while i < n and text[i].isdigit(): i += 1
				yield Token(start, i, type=NUMBER)
			continue

		# Line comment
		if text[i:i+linecomment_len] == line_comment:
			start = i
			i = text.find('\n', i+2) + 1 or n; 
			yield Token(start, i, type=LINE_COMMENT)
			continue

		# Block comment
		if text[i:i+opening_len] == block_opening:
			start = i
			depth, i = 1, i + opening_len
			while i < n and depth:
				if text[i:i+opening_len] == block_opening: depth += 1; i += opening_len
				elif text[i:i+closing_len] == block_closing: depth -= 1; i += closing_len
				else: i += 1
			yield Token(start, i, type=BLOCK_COMMENT)
			continue

		# Delimited literal
		if c in delimited_constructs:
			block_closing, i = delimited_constructs[c], i+1
			while i < n:
				if text[i] == block_closing and text[i+1:i+2] != block_closing: i += 1; break
				i += 2 if text[i:i+2] == block_closing*2 else 1
			yield Token(start, i, type=DELIMITED_LITERAL); continue

		# Operator / delimiter
		if text[i:i+2] in operators2chars:
			yield Token(i, i+2, type=OPERATOR); i += 2
		elif c in operators1char:
			yield Token(i, i+1, type=DELIMITER); i += 1
		else:
			yield Token(i, i+1, type=DELIMITER); i += 1
