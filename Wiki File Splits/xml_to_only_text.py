import xml.etree.ElementTree as ET
import os

def split_text(text, size_limit):
    """Splits the text into chunks of approximately size_limit bytes."""
    words = text.split()
    current_chunk = []
    current_size = 0
    for word in words:
        current_size += len(word) + 1  # +1 for the space or newline
        if current_size > size_limit:
            yield ' '.join(current_chunk)
            current_chunk = [word]
            current_size = len(word) + 1
        else:
            current_chunk.append(word)
    if current_chunk:
        yield ' '.join(current_chunk)

def process_xml(xml_file, output_dir, size_limit):
    """Processes the XML file and outputs smaller text files."""
    context = ET.iterparse(xml_file, events=("end",))
    page_text = []
    for event, elem in context:
        if elem.tag.endswith('text'):
            if elem.text:
                page_text.append(elem.text)
        elem.clear()
        
        if elem.tag.endswith('page'):
            full_text = ' '.join(page_text)
            page_text = []

            # Split text into smaller files
            for i, chunk in enumerate(split_text(full_text, size_limit)):
                output_file = os.path.join(output_dir, f"output_{i}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(chunk)

    del context

if __name__ == "__main__":
    xml_file = "/home/vishnu/Desktop/wiki/enwiki-20231220-pages-articles-multistream.xml"
    output_dir = "/home/vishnu/Desktop/wiki/wikichunks_txtv1"
    size_limit = 1 * 1024 * 1024  # 1MB
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    process_xml(xml_file, output_dir, size_limit)
