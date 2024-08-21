import os

CHUNK_SIZE = 1024 * 1024
cur_size = 0
MAX_SIZE = 1 * 1024 * 1024  # 10 mb
cur_idx = 0
cur_file = None
FMT = "wikichunk_%d.txt"
input_xml_file = '/home/vishnu/Desktop/wiki/enwiki-20231220-pages-articles-multistream.xml'
output_directory = '/home/vishnu/Desktop/wiki/wikichunks_txt'


def next_file():
    """This makes the decision to cut the current file and start a new one"""
    global cur_size, cur_file, cur_idx
    if cur_size > MAX_SIZE:
        print("Part %d done" % cur_idx)
        cur_file.close()
        cur_size = 0
        cur_idx += 1
        cur_file = open(os.path.join(output_directory, FMT % cur_idx), 'wt', encoding='utf-8')


def main():
    try:
        global cur_file, cur_idx, cur_size

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        cur_file = open(os.path.join(output_directory, FMT % cur_idx), 'wt', encoding='utf-8')

        with open(input_xml_file, 'rt', encoding='utf-8') as xml_file:
            while True:
                chunk = xml_file.read(CHUNK_SIZE)
                if len(chunk) < CHUNK_SIZE:
                    cur_file.write(chunk)
                    break
                cur_file.write(chunk)
                cur_size += len(chunk)
                next_file()

        cur_file.close()
        print("Part %d done" % cur_idx)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
