class AoCParser:
    def __init__(self, abs_input_filepath):
        self.abs_input_filepath = abs_input_filepath

    def parse_as_2d_list(self):
        ret = []  
        with open(self.abs_input_filepath, 'r') as inputfp:
            line = inputfp.readline()
            while(line):
                ret.append([char for char in line.strip()])
                line = inputfp.readline()
        return ret

    def parse_as_list_of_ints(self):
        ret = []
        with open(self.abs_input_filepath, 'r') as inputfp:
            line = inputfp.readline()
            while(line):
                ret.append(int(line))
                line = inputfp.readline()
        return ret

    def parse_as_list_of_strings(self):
        ret = []
        with open(self.abs_input_filepath, 'r') as inputfp:
            line = inputfp.readline()
            while(line):
                ret.append(line.strip())
                line = inputfp.readline()
        return ret

    def parse_as_list_of_paragraphs(self):
        ret = []
        with open(self.abs_input_filepath, 'r') as inputfp:
            paragraph = []
            line = inputfp.readline()
            while(line):
                if line == "\n":
                    ret.append(paragraph)
                    paragraph = []
                else:
                    paragraph.append(line.strip())
                line = inputfp.readline()
            if len(paragraph) > 0:
                ret.append(paragraph)
        return ret