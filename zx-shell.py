from cmd import Cmd
import sys
import os
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_for_filename
from pygments.styles import get_style_by_name

class ZXShell(Cmd):
    intro  = "    Retro style shell inspired by ZX Spectrum\n          Type 'help' to list commands\n"
    prompt = '>>> '
    lines=[]
    lexer=Python3Lexer()

    def do_quit(self, line):
        '''Exit the shell'''
        if len(self.lines): self.lines.pop()
        sys.exit(0)
    
    def do_list(self, line):
        '''List source code'''
        if len(self.lines): self.lines.pop()
        for index in range(len(self.lines)):
            print('%03d'%(index + 1),
                   highlight(self.lines[index],
                             self.lexer,
                             Terminal256Formatter()),
                   end='')
    
    def do_insert(self, line):
        '''Insert line at given index, e.g. "insert 10 some code"'''
        if len(self.lines): self.lines.pop()
        self.lines.insert(int(line.split()[0])-1, ''.join(line.split()[1:]))
    
    def do_exec(self, line):
        '''Run OS command, e.g. "python3 test.py"'''
        if len(self.lines): self.lines.pop()
        os.system(line)
    
    def do_clear(self, line):
        '''Clear console'''
        if len(self.lines): self.lines.pop()
        os.system('clear')
    
    def do_new(self, line):
        '''Start new session'''
        self.lines = ['']
        self.do_clear('')
    
    def do_save(self, line):
        '''Save file, e.g. "save file.txt"'''
        if len(self.lines): self.lines.pop()
        try:
            with open(line.split()[0], 'w') as f: f.write('\n'.join(self.lines))
            print('File "' + line.split()[0] + '" has been successfully saved!')
        
        except:
            print('Usage: save file.txt')
    
    def do_load(self, line):
        '''Load file, e.g. "load file.txt"'''
        if len(self.lines): self.lines.pop()
        try:
            with open(line.split()[0]) as f: self.lines = f.read().split('\n')
            self.lexer = get_lexer_for_filename(line.split()[0])
            print('File "' + line.split()[0] + '" has been successfully loaded!')
            
        except:
            print('Usage: load file.txt')
    
    def do_edit(self, line):
        '''Edit line, e.g. edit 3 [would edit line #3]'''
        if len(self.lines): self.lines.pop()
        try:
            self.lines[int(line.split()[0]) - 1] = line[line.index(' ') + 1:]
            
        except:
            print('Usage: edit 3 new content [would replace line 3 (if exists) with "new content"]')
    
    def do_delete(self, line):
        '''Delete line, e.g. delete 3 [would delete line#3]'''
        if len(self.lines): self.lines.pop()
        try:
            del self.lines[int(line.split()[0]) - 1]

        except:
            print('Usage: delete 3 [would delete line 3 (if exists)')
            
    def precmd(self, line):
        if not len(line.split()): self.lines.append('')
        elif line.split()[0] != 'help': self.lines.append(line)
        return line
    
    def emptyline(self):
        pass
        
    def default(self, line):
        pass
    
    do_EOF = do_quit
 
if __name__ == '__main__':
    os.system('clear')
    shell = ZXShell()
    shell.cmdloop()
    
