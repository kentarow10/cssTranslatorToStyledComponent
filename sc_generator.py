# -*- coding: utf-8 -*-
import sys
import re
from collections import defaultdict

class Parent:
    def __init__(self,key,value):
        self.coron = False
        self.cssWithCoron = defaultdict(str)
        self.wCoron = False
        self.cssWithWcoron = defaultdict(str)
        self.key = key
        if '::' in key:
            splited = key.split("::")
            self.wCoron = True
            self.cssWithWcoron[splited[1]] = value
            self.key = splited[1]
        elif ':' in key:
            splited = key.split(":")
            self.coron = True
            self.cssWithCoron[splited[1]] = value
            self.key = splited[1]
        else:
            print("something wrong...")
    def returnParentName(self):
        if self.wCoron:
            return "&::" + self.key
        elif self.coron:
            return "&:" + self.key
        else:
            return "something wrong..."

class Child:
    def __init__(self,key,value):
        self.className = ""
        self.css = value
        self.coron = False
        self.cssWithCoron = defaultdict(str)
        self.key = key
        self.wCoron = False
        self.cssWithWcoron = defaultdict(str)
        if '::' in key:
            splited = key.split("::")
            self.className = splited[0].capitalize()
            self.wCoron = True
            self.cssWithWcoron[splited[1]] = value
            self.key = splited[1]
        elif ':' in key:
            splited = key.split(":")
            self.className = splited[0].capitalize()
            self.coron = True
            self.cssWithCoron[splited[1]] = value
            self.key = splited[1]
        else:
            self.className = key
    def returnChildPart(self):
        if self.wCoron:
            return """${{{0}}}::{1}{{
    {2}
}}""".format(self.className,self.key,self.cssWithWcoron[self.key])
        elif self.coron:
            return """${{{0}}}::{1}{{
    {2}
}}""".format(self.className,self.key,self.cssWithCoron[self.key])
        else:
            return """err::after{
    something wrong
}"""

class PCPair:
    def __init__(self,k,v):
        firstHalf = k.split(" ")[0]
        secondHalf = k.split(" ")[1]
        self.parent = Parent(firstHalf,v)
        self.child = Child(secondHalf,v)
    def genCode(self):
        p = self.parent.returnParentName()
        c = self.child.returnChildPart()
        code = """
{} {{
{}
}}
""".format(p,c)
        return code

class ClassUnit:
    def __init__(self,key,value):
        self.className = key
        self.css = value
        self.coron = False
        self.cssWithCoron = defaultdict(str)
        self.wCoron = False
        self.cssWithWcoron = defaultdict(str)
        self.containDeps = False
        self.pc = None
    def update(self,key,value):
        if " " in key:
            self.pc = PCPair(key,value)
            self.containDeps = True
        elif '::' in key:
            splited = key.split("::")
            self.wCoron = True
            self.cssWithWcoron[splited[1]] = value
        elif ':' in key:
            splited = key.split(":")
            self.coron = True
            self.cssWithCoron[splited[1]] = value
    def generate(self):
        coronPart = ""
        wCoronPart = ""
        pcPart = ""
        if self.coron:
            for k,v in self.cssWithCoron.items():
                v = v.strip()
                part = """
&:{} {{
{}
}}                
""".format(k,v)
                coronPart = coronPart + part
        if self.wCoron:
            for k,v in self.cssWithWcoron.items():
                v = v.strip()
                wPart = """
&::{} {{
{}
}}
""".format(k,v)
                wCoronPart = wCoronPart + wPart
        if self.containDeps:
            pcPart = self.pc.genCode()

        css = self.css.strip()
        codes = """
export const {} = styled.div`
{}
{}
{}
{}
`
""".format(self.className, css, coronPart, wCoronPart, pcPart)

        return codes

class StyledComponentGenerateManager:
    def __init__(self):
        self.classUnits = []
        self.isAppeared = defaultdict(bool)
    def inputKeyValue(self,key,value):
        sheerKey = key
        if " " in key:
            sheerKey = key.split(" ")[0]
        if ":" in sheerKey:
            sheerKey = sheerKey.split(":")[0]
        for cu in self.classUnits:
            if cu.className == sheerKey:
                cu.update(key,value)
                return
        self.classUnits.append(ClassUnit(key,value))
        self.isAppeared[sheerKey] = False
    def output(self,path):
        output = "import styled from 'styled-components';"
        waitings = []
        for u in self.classUnits:
            self.isAppeared[u.className] = True
            if u.containDeps and not self.isAppeared[u.pc.child.className]:
                waitings.append(u)
            else:
                output += u.generate()
        for u in waitings:
            output += u.generate()
        with open(path, mode='w') as f:
            f.write(output)

def toUpperOnlyFirstChar(name):
    ch = name[0].upper()
    name = ch + name[1:]
    return name

def main():
    args = sys.argv
    if 2 != len(args):
        print("Give me an input CSS file name as an argument!!!")
        return

    in_path = "./input/" + args[1] + ".css"
    out_path = "./output/" + args[1] + ".ts"

    with open(in_path) as inf:
        contents = inf.read()

    keys = []
    values = []
    pre_char = ""
    values_mode = False

    for char in contents:
        if char == "{":
            keys.append(pre_char)
            values_mode = True
            pre_char = ""
        elif char == "}":
            values.append(pre_char)
            values_mode = False
            pre_char = ""
        elif values_mode:
            pre_char = pre_char + char
        else:
            pre_char = pre_char + char

    keys2 = []
    values2 = []
    for i, k in enumerate(keys):
        k.replace("\n","")
        if "," in k:
            splited = k.split(",")
            for splitedk in splited:
                keys2.append(splitedk)
                values2.append(values[i])
        else:
            keys2.append(k)
            values2.append(values[i])

    del keys, values

    scgm = StyledComponentGenerateManager()
    for k,v in zip(keys2,values2):
        k = k.replace('\n','')
        k = k.replace('.','')
        k = k.replace('-','_')
        k = k.strip()
        name = toUpperOnlyFirstChar(k)
        v = v.strip()
        scgm.inputKeyValue(name,v)

    scgm.output(out_path)

if __name__ == "__main__":
    main()
