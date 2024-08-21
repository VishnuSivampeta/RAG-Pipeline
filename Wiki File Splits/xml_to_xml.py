import os
import xml.parsers.expat
from xml.sax.saxutils import escape
from math import log10

CHUNK_SIZE = 1024 * 1024
path = []
cur_size = 0
MAX_SIZE = 10 * 1024 * 1024  # 10 mb
cur_idx = 0
cur_file = None
FMT = ".%d"
out_dir = None
root = None
ext = None
xml_declaration = None
start = None
ending = False
input_xml_file = '/mnt/datastore/wikipedia/enwiki-20231220-pages-articles-multistream.xml'
output_directory = '/mnt/datastore/wikipedia/wikichunks'

def attrs_s(attrs):
    """This generates the XML attributes from an element attribute list"""
    l = ['']
    for i in range(0, len(attrs), 2):
        l.append('%s="%s"' % (attrs[i], escape(attrs[i + 1])))
    return ' '.join(l)

def next_file():
    """This makes the decision to cut the current file and start a new one"""
    global cur_size, ending
    if (not ending) and (cur_size > MAX_SIZE):
        global cur_file, cur_idx
        print("Part %d done" % cur_idx)
        ending = True

        for elem in reversed(path):
            end_element(elem[0])

        cur_file.close()
        cur_size = 0
        cur_idx += 1

        cur_file = open(os.path.join(out_dir, root + FMT % cur_idx + ext), 'wt', encoding='utf-8')
        if xml_declaration is not None:
            cur_file.write('<?xml%s?>\n' % attrs_s(xml_declaration))
        for elem in path:
            start_element(*elem)
        ending = False

def xml_decl(version, encoding, standalone):
    global xml_declaration
    l = ['version', version, 'encoding', encoding]
    if standalone != -1:
        l.extend(['standalone', 'yes' if standalone else 'no'])
    xml_declaration = l
    cur_file.write('<?xml%s?>\n' % attrs_s(xml_declaration))

def start_element(name, attrs):
    """Called by the parser when it meets a start element"""
    global cur_size, start
    if start is not None:
        cur_file.write('<%s%s>' % (start[0], attrs_s(start[1])))
    start = (name, attrs)
    if ending:
        return
    cur_size += len(name) + sum(len(k) for k in attrs)
    path.append((name, attrs))

def end_element(name):
    """Called by the parser when it meets an end element"""
    global cur_size
    global start
    if start is not None:
        cur_file.write('<%s%s/>' % (start[0], attrs_s(start[1])))
    else:
        cur_file.write('</%s>' % name)
    start = None
    if ending:
        return
    elem = path.pop()
    assert elem[0] == name
    cur_size += len(name)
    next_file()

def char_data(data):
    """Called by the parser when it meets data"""
    global cur_size, start
    wroteStart = False
    if start is not None:
        cur_file.write('<%s%s>' % (start[0], attrs_s(start[1])))
        start = None
        wroteStart = True

    data = data.replace('&', '&amp;')
    data = data.replace('<', '&lt;')
    if data == '>':
        data = '&gt;'
    cur_file.write(data)
    cur_size += len(data)
    if not wroteStart:
        next_file()

def main():
    try:
        p = xml.parsers.expat.ParserCreate()
        p.ordered_attributes = 1
        p.XmlDeclHandler = xml_decl
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        global cur_file, cur_idx
        global out_dir, root, ext
        global FMT

        FMT = ".%%0%dd" % (int(log10(os.path.getsize(input_xml_file) / MAX_SIZE)) + 1)

        out_dir, filename = os.path.split(input_xml_file)
        if output_directory is not None:
            out_dir = output_directory

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        root, ext = os.path.splitext(filename)

        cur_file = open(os.path.join(out_dir, root + FMT % cur_idx + ext), 'wt', encoding='utf-8')

        with open(input_xml_file, 'rt', encoding='utf-8') as xml_file:
            while True:
                chunk = xml_file.read(CHUNK_SIZE)
                if len(chunk) < CHUNK_SIZE:
                    p.Parse(chunk, 1)
                    break
                p.Parse(chunk)

        cur_file.close()
        print("Part %d done" % cur_idx)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
