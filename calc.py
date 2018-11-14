#!/usr/bin/env python2
#Christopher Lynch
#Section 004, Professor Kurt Schmidt
#11/14/2018

#This script expressions from the user, converts from infix expressions to postfix expressions, and evaluates. 

import sys


def main():

#This section will collect the input and then format it into a list of strings

	if len(sys.argv) == 1: #Case where stdin was used
		f = sys.stdin.readlines()

	elif len(sys.argv) == 2: #Case where a file was used
		try:
			f = open(sys.argv[1],'r').readlines()
		except IOError: #Throw an error if program can't find the file name given.
			print("Please enter a valid file name")
			sys.exit(1)

	formattedInput = []
	i = 0
	for line in f: #This loop goes through all the input and puts it into a list of lists, one list of strings for each problem inputted
		line = line.split(" ")
		for element in line:
			line[i] = element.strip('\n')
			i = i + 1
		i = 0
		formattedInput.append(line)

#This loop uses the infix2postfix() and evalPostfix() functions on the formatted input, then prints result.
	for item in formattedInput:
		postfixItem = infix2postfix(item)
		postfixItemString = ''
		for character in postfixItem:
			postfixItemString = postfixItemString + ' ' + character
		finalString = postfixItemString + ' = ' + str(evalPostfix(postfixItem))
		print(finalString.strip())


def getPrecedence(operator): #Helper function to give an integer representing operator precedence
	if operator in '+-':
		return 1
	else:
		return 2

#This section implements a simple stack for evaluation purposes
class Stack: 
	def __init__(self):
		self.stack = []
	
	def push(self,item):
		self.stack.append(item)
	
	def pop(self):
		self.stack.pop()

	def top(self):
		return str(self.stack[len(self.stack)-1])

#This function converts the infix expressions to postfix, and returns a list of characters
def infix2postfix(expression):
	in2postResult = []
	in2postStack = Stack()	
	expression.append(')')
	in2postStack.push('(')

	for token in expression:

		if token == '(': #Parenthesis case
			in2postStack.push(token)

		elif token == ')': #Parenthesis case 
			while in2postStack.top() != '(':
				in2postResult.append(in2postStack.top())
				in2postStack.pop()
			in2postStack.pop()

		elif token in '-+*/%': #Token is an operator case
			while (getPrecedence(in2postStack.top()) >= getPrecedence(token)) and (in2postStack.top() in '+-*/%'): #Use getPrecedence helper
				in2postResult.append(in2postStack.top())
				in2postStack.pop()
			in2postStack.push(token)

		else: #Final case is token is a number (operand)
			in2postResult.append(token)

	return in2postResult

#This function takes an expression in postfix, and returns an integer as the result
def evalPostfix(expression):
	evalPostStack = Stack()

	for token in expression:

		if token in '+-*/%': #Token is an operator case
			y = int(evalPostStack.top())
			evalPostStack.pop()
			x = int(evalPostStack.top())
			evalPostStack.pop()

			if token == '-':
				result = (x-y)
			elif token == '+':
				result = (x+y)
			elif token == '/':
				result = (x/y)
			elif token == '*':
				result = (x*y)
			else:
				result = (x%y)

			evalPostStack.push(result)

		else: #Token is a number (operand)
			evalPostStack.push(token)

	return result #Result will be an int

main()
