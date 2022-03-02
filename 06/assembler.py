import re
from typing import Optional, List

# DONE 1) Parser
# 2) Code translator
# 3) Symbol Table
# 4) "main"


# What can we expect?

# A-Instructions:
#   @<numeric literal>
#   @<symbol>

# C-Instructions:
#   <dest>=<comp>[;<jump>]  (if there's a destination and computation, then jump is optional) 
#   <comp>;<jump>           (if there is no destination, then compute and jump are mandatory)

# Labels:
#   (<label name>)          (always starts with a parenthesis, always refers to the program line below the current line. Don't count labels as program lines themselves)


# Parsing:
# What are our acceptable token types?
# dest, comp, jmp, "111", label, a_symbol, a_numliteral



# Other notes:
# 1) first pass, look for all labels (<label name>)
# 2) second pass, actually start parsing / doing look ups
#   2a) If you run into an A-instruction for a symbol you don't have in your symbol table (@<symbol>), then add it starting at 16 and onward


# Other thoughts:
# What even is a symbol? A symbol can take two general forms:
# 1) a label: this is a specific instruction within our program that we refer to with a number (every instruction is numbered)
# 2) a variable: this is a memory register that holds some value that we want to refer to later on
# Our hack computer makes a clear distinction between ROM (where our program lives) and RAM (where our data lives). But
# how is this represented in the symbol table of our assembly language? It seems like once things get added to the
# symbol table, you can no longer tell if they came from a label or a variable?



class Assembler():

    def __init__(self):
        self.symbol_table = self._populate_initial_symbol_table()
        self.instruction_number = 0
        self._populate_lookup_tables()  # side effects
    
    
    def assemble(self, file_in: str, file_out: Optional[str] = None):
        """
        I put all the nasty side effects (disk IO) right here so that
        all the other functions are as testable as possible.
        """
        
        # read data
        with open(file_in, "r") as f:
            file_contents = f.read()
        
        if not file_out:
            file_out = re.sub(r"\.asm$", ".hack", file_in)

        # write the output
        with open(file_out, "w") as f:
            f.write(self.main(file_contents))
        
        return
            

    def main(self, file_contents: str) -> str:

        # remove whitespace from all lines
        lines = self._remove_whitespace(file_contents)

        # first pass and parsing (this will add labels to symbol table)
        parsed = []
        for line in lines:
            if line:
                parsed.append(self.parse_line(line))
        
        # second pass, here we'll resolve symbols to their memory values;
        # implementation detail, symbols start at memory register 16 onwards;
        output_lines = []
        self.new_variable_memory_position = 16
        for line in parsed:
            this_binary_line = self.code_lookup(line)
            if this_binary_line:
                output_lines.append(this_binary_line)
        
        return "\n".join(output_lines)


    def parse_line(self, line: str) -> dict:
        """
        Side effect: This will add labels to the symbol table as it parses each line. That
                    will effectively count as our "first pass".

        TODO: I'm mixing too much in here. I need a first_pass method that does the
            instruction number counting and adds labels to the symbol table. That
            shouldn't be something I try and do here, should it? Need to think 
            that through a bit more.

            Actually. Maybe I can do the first pass in this function?
        """
        if line[0] == "@":

            # A-instruction
            self.instruction_number += 1
            line = re.sub("@", "", line)
            if line.isdigit():
                return {"type": "A-instruction-literal", "a_numliteral": line}
            else:
                return {"type": "A-instruction-symbol", "a_symbol": line}

        elif line[0] == "(":

            # Label 
            line = re.sub(r"^\(", "", line)
            line = re.sub(r"\)$", "", line)
            self.symbol_table[line] = self.instruction_number
            return {"type": "label", "label": line, "value": self.instruction_number}

        else:

            # C-instruction
            self.instruction_number += 1

            # destination
            if "=" in line:
                dest, line = line.split("=")
            else:
                dest = "null"
            
            # computation and jump
            if ";" in line:
                comp, jump = line.split(";")
            else:
                comp = line
                jump = "null"
            
            return {"type": "C-instruction", "dest": dest, "comp": comp, "jump": jump}


    def code_lookup(self, codes: dict) -> str:
        """
        Args:
            - codes: a dictionary that represents the parsed assembly instruction
        
        Returns:
            - a binary string representing the components of the instruction in machine code.
        """

        type = codes.get("type")
        

        if type == "A-instruction-literal":

            return self._int_to_bin(codes.get("a_numliteral"))
        

        elif type == "A-instruction-symbol":

            symbol = codes.get("a_symbol")
            
            if symbol in self.symbol_table:
                # symbol was already in the table. convert it to binary string and return it.
                return self._int_to_bin(self.symbol_table[symbol])
            
            else:
                # symbol didn't exist in table. add it, increment new variable memory location.
                self.symbol_table[symbol] = self.new_variable_memory_position
                self.new_variable_memory_position += 1
                return self._int_to_bin(self.symbol_table[symbol])
        

        elif type == "C-instruction":
            
            dest = self.lookup_destination.get(codes["dest"])
            comp = self.lookup_computation.get(codes["comp"])
            jump = self.lookup_jump.get(codes["jump"])

            if not dest:
                dest = "000"
            
            if not jump:
                jump = "000"

            return "".join(["111", comp, dest, jump])


    def _populate_lookup_tables(self):
        """
        Side effects. Directly assigns class attributes
        """

        self.lookup_destination = {
            "null": "000",
            "M":    "001",
            "D":    "010",
            "MD":   "011",
            "A":    "100",
            "AM":   "101",
            "AD":   "110",
            "AMD":  "111"
        }

        self.lookup_computation = {
            "0":    "0101010",
            "1":    "0111111",
            "-1":   "0111010",
            "D":    "0001100",
            "A":    "0110000",
            "M":    "1110000",
            "!D":   "0001101",
            "!A":   "0110001",
            "!M":   "1110001",
            "-D":   "0001111",
            "-A":   "0110011",
            "-M":   "1110011",
            "D+1":  "0011111",
            "A+1":  "0110111",
            "M+1":  "1110111",
            "D-1":  "0001110",
            "A-1":  "0110010",
            "M-1":  "1110010",
            "D+A":  "0000010",
            "D+M":  "1000010",
            "D-A":  "0010011",
            "D-M":  "1010011",
            "A-D":  "0000111",
            "M-D":  "1000111",
            "D&A":  "0000000",
            "D&M":  "1000000",
            "D|A":  "0010101",
            "D|M":  "1010101"
        }

        self.lookup_jump = {
            "JGT":  "001",
            "JEQ":  "010",
            "JGE":  "011",
            "JLT":  "100",
            "JNE":  "101",
            "JLE":  "110",
            "JMP":  "111"
        }


    def _populate_initial_symbol_table(self) -> dict:

        # start with R0, R1, ... R15
        symbol_table = {"".join(["R", str(x)]): x for x in range(0, 16)}

        # then update
        symbol_table.update({
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4
        })

        return symbol_table


    def _remove_whitespace(self, file_contents: str) -> List[str]:
        """

        Args:
            - file_contents: the string contents of a file, not yet
                split into lines
        
        Returns:
            The original file contents with no white-space or comments.

        Parses the contents of a Hack .asm file. Specifically, this
        function will filter out comments and remove all white-space,
        leaving just the resulting assembly code instructions.
        """

        # Steps:
        # 1. split into a list of strings based on newline character
        # 2. if you see "//" on a line, remove that and everything after it
        # 3. remove all whitespace remaining
        # 4. remove any lines that now might be empty strings
        lines = file_contents.split("\n")
        lines = [re.sub(r"//.*", "", x) for x in lines]
        lines = [re.sub(" *", "", x) for x in lines]
        lines = [x for x in lines if x]

        # join the lines together with a new-line separator
        # content_no_whitespace = "\n".join(lines)

        return lines


    def _int_to_bin(self, int_string: str, total_chars: int = 16) -> str:
        """
        Converts a string representing a decimal integer into
        a string representing that same number in binary.
        """

        this_int = int(int_string)
        in_binary = bin(this_int)
        in_binary = re.sub("b", "", in_binary)
        in_binary = in_binary.zfill(total_chars)

        return in_binary




if __name__ == "__main__":

    import os
    os.chdir("06")

    a = Assembler()
    a.assemble("max/Max.asm")

    a = Assembler()
    a.assemble("pong/Pong.asm")

