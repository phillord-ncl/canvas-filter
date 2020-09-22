__version__ = '0.1.0'

import os
import tempfile
import toml


from panflute import *

def codefilter(elem, doc):
    ##print(elem, file=open("log.txt", "a"))
    if type(elem) == CodeBlock:
        lang = elem.classes[0]
        include=elem.attributes.get("include")
        output=elem.attributes.get("output")

        if not include:
            fd, path = tempfile.mkstemp(text=True)
            f = open(path, "w")
            f.write(elem.text)
            f.flush()

        stream = os.popen(
            "source-highlight -n " +
            "--src-lang=" + lang +
            " -o STDOUT -i " +
            (include or path), "r"
        )

        highlighted = stream.read()

        if not include:
            f.close()

        if include:
            include_url = "../files/{}/download".format(str(toml.load(include + ".tpf").get("id")))

        if output:
            name = os.path.splitext(include)[0]
            with open(name + ".out" ) as fh: output_text = fh.read()
            fh.close()


        return [i for i in
                [
                    RawBlock(highlighted),
                    include and Para(Link(Str("Take from: " + include),
                                          url=include_url)),
                    output and CodeBlock(output_text)
                ]
                if i
        ]

def main(doc=None):
    print("main", file=open("log.txt", "a"))
    return run_filter(codefilter, doc=doc)

if __name__ == '__main__':
    main()
