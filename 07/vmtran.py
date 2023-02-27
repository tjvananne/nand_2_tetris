# My VM Translator for Ch 7 of Nand2Tetris

# Thoughts: 
# So the command types (C_ARITHMETIC, C_POP, C_PUSH, etc) are all there
# mostly for determining which of the writer methods we need to call. 
# But then, once we know which one to call, we can pass in the actual
# raw command string.


from collections import deque
import re
import sys
import logging
from typing import List
logging.basicConfig(level=logging.DEBUG)

TEMP_ADDR_OFFSET = 5

class Parser():
    """
    Reads the .vm file, removes whitespace and comments, and parses
    the file into lexical components.
    
    API:
    - has_more_commands: returns True if there is 1 or more commands left to be parsed
    - command_type: returns str of command type (ex: C_ARITHMETIC, C_POP, C_PUSH, etc)
    - advance: moves to the next command in the vm script
    - arg1: property containing the first argument (if applicable)
    - arg2: property containing the second argument (if applicable)
    """

    def __init__(self, vm_filename):

        self.current_command = None
        self._command_type = None
        self.arg1 = None
        self.arg2 = None

        logging.info(f"Reading {vm_filename}")
        with open(vm_filename, 'r') as f:
            self.vm_lines: List[str] = f.readlines()
        logging.debug(''.join(self.vm_lines))
        self.vm_lines = self._remove_whitespace_comments()

        logging.debug("\n\nprinting lines after removing whitespace and comments")
        logging.debug('\n'.join(self.vm_lines))


    @property
    def has_more_commands(self) -> bool:
        """property so we can access with <parser>.has_more_commands"""
        return bool(len(self.vm_lines))


    @property
    def command_type(self) -> str:
        cmd = self.command_tokens[0]
        if cmd in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'C_ARITHMETIC'
        elif cmd == 'pop':
            return 'C_POP'
        elif cmd == 'push':
            return 'C_PUSH'
        # TODO: implement the other command types
        else:
            raise Exception(f"Invalid command: {cmd}")


    def advance(self):
        """Moves to the next VM command"""
        self.current_command = self.vm_lines.popleft()
        self.command_tokens = str.split(self.current_command, ' ')
        self.arg1 = str(self.command_tokens[1]) if len(self.command_tokens) > 1 else None
        self.arg2 = int(self.command_tokens[2]) if len(self.command_tokens) > 2 else None


    def _remove_whitespace_comments(self) -> deque[str]:
        clean_lines = deque()
        for line in self.vm_lines:

            line = re.sub('//.*', '', line)
            line = line.strip()
            if line != '':
                clean_lines.append(line)

        return clean_lines



class CodeWriter():

    def __init__(self, asm_filename: str, vm_filename: str):

        self.vm_filename = vm_filename  # for naming static variables
        self.output_file = open(asm_filename, 'w')
        self._segment_map = {
            # pointers to base addresses in RAM
            'local': 'LCL',
            'argument': 'ARG',
            'that': 'THAT',
            'this': 'THIS',
            # base address of temp is always the same
            'temp': TEMP_ADDR_OFFSET,
            # segment names don't change/matter
            'constant': 'constant',
            'static': 'static',
        }

    def write_arithmetic(self, cmd: str) -> None:
        # figure out the assembly to be written and write it to the output file
        # write the raw command as a comment to the file
        self.output_file.write(self._generate_asm_comment_cmd(cmd)) 
        pass

    def write_push_pop(self, cmd: str, segment: str, idx: int) -> None:
        # figure out the assembly to be written and write it to the output file
        # write the raw command as a comment to the file
        self.output_file.write(self._generate_asm_comment_cmd(cmd)) 
        
        if cmd.startswith('pop'):
            asm_code = '\n'.join(self._generate_asm_pop(cmd, segment, idx))
        elif cmd.startswith('push'):
            asm_code = '\n'.join(self._generate_asm_push(cmd, segment, idx))
        else:
            raise Exception(f"Push pop command not recognized: {cmd}")        
        self.output_file.write(asm_code)


    def _generate_asm_pop(self, cmd: str, segment: str, idx: int) -> List[str]:
        """
        Generates the assembly based on the passed in arguments.

        - cmd: the full command, such as `pop local 2`
        - segment: just the segment, such as `local`
        - idx: just the index value, such as `2`

        Pseudo code for `pop local 2`:
        addr=LCL+2, SP--, *addr=*SP

        NOTE: You cannot pop into constant. That wouldn't make sense.
        LCL, ARG, THIS, THAT all behave the same.
        Static requires special treatment (store as variable with special name).
        Temp requires special treatment (base address is always 5?)
        """

        # Mapping and error handling
        if segment == 'constant':
            raise Exception(f"Can't pop to constant: {cmd}")

        segment = self._segment_map[segment]
        if segment in ['LCL', 'ARG', 'THIS', 'THAT', TEMP_ADDR_OFFSET]:
            addr = '@addr'
        elif segment == 'static':
            addr = self._generate_asm_static_var_name(idx)
        else:
            raise Exception(f"Unrecognized segment: {segment}")

        # Build asm
        asm_out = []
        asm_out.extend(self._generate_asm_address_offset(segment, idx))
        asm_out.extend(self._generate_asm_sp_dec())
        asm_out.extend(self._generate_asm_pop_to_addr(addr))
        # asm_out.append('\n')
        return asm_out


    def _generate_asm_push(self, cmd: str, segment: str, idx: int) -> List[str]:
        """TODO"""

        # Mapping and error handling
        segment = self._segment_map[segment]
        is_constant = segment == 'constant'
        if is_constant:
            addr = f"@{idx}"
        elif segment in ['LCL', 'ARG', 'THIS', 'THAT', TEMP_ADDR_OFFSET]:
            addr = '@addr'
        elif segment == 'static':
            addr = self._generate_asm_static_var_name(idx)
        else:
            raise Exception(f"Unrecognized segment: {segment}")
        
        asm_out = []
        if not is_constant:
            asm_out.extend(self._generate_asm_address_offset(segment, idx))
        asm_out.extend(self._generate_asm_push_to_stack(addr, is_constant))
        asm_out.extend(self._generate_asm_sp_inc())
        # asm_out.append('\n')
        return asm_out


    def _generate_asm_address_offset(self, segment: str, idx: int) -> List[str]:
        """Generates the asm to store the segment address in @addr"""
        return [
            "// calculating address offset",
            f"@{segment}",
            "D=M",     # store segment offset in D register
            "@addr",   # create/select the @addr variable
            "M=D",     # set @addr to segment offset
            f"@{idx}", # select the index as a constant
            "D=A",     # store index constant value in data register
            "@addr",   # select @addr variable
            "M=D+M",   # add the index offset to @addr, store in @addr
            ""
        ]
        

    def _generate_asm_static_var_name(self, idx: int) -> str:
        return ''.join(['@', self.vm_filename, '.', str(idx)])


    def _generate_asm_pop_to_addr(self, addr_var):
        """
        addr_var is the name of a variable including the '@' symbol.
        """
        return [
            f"// popping value to address {addr_var}",
            "@SP",
            "D=M",
            addr_var,
            "M=D",
            ""
        ]



    def _generate_asm_push_to_stack(self, addr_var: str, is_constant = False) -> List[str]:
        """
        addr_var is the name of a variable including the '@' symbol.
        You can pass constants in through addr_var as well.

        Ex: `push constant 42` can be expressed by `addr_var=@42` and `is_constant=True`
        """
        from_value = 'A' if is_constant else 'M'
        return [
            f"// pushing value to stack from {addr_var}",
            addr_var,
            f"D={from_value}",
            "@SP",
            "M=D",
            ""
        ]

    def _generate_asm_sp_dec(self) -> List[str]:
        return ['// decrementing stack pointer', '@SP', 'M=M-1', '']

    def _generate_asm_sp_inc(self) -> List[str]:
        return ['// incrementing stack pointer', '@SP', 'M=M+1', '']
    
    def _generate_asm_comment_cmd(self, cmd) -> List[str]:
        return ' '.join(['\n//', '=' * 20, cmd, '=' * 20, '\n'])

    def close(self):
        self.output_file.close()


class Main():
    def __init__():
        pass


if __name__ == "__main__":
    logging.debug(f"program arguments: {sys.argv}")
    vm_filename = sys.argv[1]
    parser = Parser(vm_filename)
    writer = CodeWriter(asm_filename='./07/MemoryAccess/BasicTest/BasicTest.asm', vm_filename=vm_filename)
    print(f"has more commands? {parser.has_more_commands}")
    while parser.has_more_commands:
        parser.advance()
        print(f"command after advancing: {parser.current_command}")
        print(f"parser command type: {parser.command_type}\targ1: {parser.arg1}\targ2: {parser.arg2}")
        if parser.command_type in ['C_PUSH', 'C_POP']:
            writer.write_push_pop(parser.current_command, parser.arg1, parser.arg2)

