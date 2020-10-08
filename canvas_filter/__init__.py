__version__ = '0.1.0'

import os
import tempfile
import toml


from panflute import *

def tpf(f):
    return toml.load(f + ".tpf")

def code_filter(elem, doc):
    print(elem, file=open("log.txt", "a"))

    lang = len(elem.classes) > 0  and elem.classes[0]
    include=elem.attributes.get("include")
    output=elem.attributes.get("output")
    stout=elem.attributes.get("stout")
    crash=elem.attributes.get("crash")

    if not include:
        fd, path = tempfile.mkstemp(text=True)
        f = open(path, "w")
        f.write(elem.text)
        f.flush()

    if lang:
        stream = os.popen(
            "source-highlight -n " +
            "--src-lang=" + lang +
            " -o STDOUT -i " +
            (include or path), "r"
        )
        highlighted = stream.read()
    else:
        print("no lang", file=open("log.txt", "a"))
        with open(include or path) as fh: content = fh.read()
        highlighted = "<pre><code>" + content + "\n</code></pre>"

    if not include:
        f.close()

    if include:
        include_url = "../files/{}/download".format(str(tpf(include).get("id")))

    if output:
        name = os.path.splitext(include)[0]
        with open(name + ".out" ) as fh: output_text = fh.read()
        fh.close()

    if stout:
        print("stout", file=open("log.txt", "a"))
        name = os.path.splitext(include)[0]
        with open(name + ".stout" ) as fh: stout_text = fh.read()
        fh.close()

    if crash:
        name = os.path.splitext(include)[0]
        with open(name + ".crash" ) as fh: crash_text = fh.read()
        fh.close()


    return [i for i in
            [
                RawBlock(highlighted),
                include and Para(Link
                                 (Str("Take from: "
                                      + os.path.basename(include)),
                                  url=include_url)),
                output and Para(Str("Outputs")),
                output and CodeBlock(output_text),
                stout and Para(Str("Prints")),
                stout and CodeBlock(stout_text),
                crash and Para(Str("Crashes")),
                crash and CodeBlock(crash_text)
            ]
            if i
        ]

def link_filter(elem, doc):
    base, ext = os.path.splitext(elem.url)
    ##print("base, ext", base, ext, file=open("log.txt", "a"))
    if ext == ".mp4":
        tpf_data = tpf(elem.url)
        print("tpf_dat", tpf_data, file=open("log.txt", "a"))
        return RawInline('''
<iframe style="width: 400px; height: 225px; display: inline-block;"
  title="Video player"
  data-media-type="video"
  src="https://ncl.instructure.com/media_objects_iframe/{uuid}?type=video"
  allowfullscreen="allowfullscreen" allow="fullscreen"
  data-media-id="{uuid}">
</iframe>
'''.format(uuid=tpf_data.get("media_entry_id")))



def canvas_filter(elem, doc):
    if type(elem) == Link:
        return link_filter(elem, doc)

    if type(elem) == CodeBlock:
        return code_filter(elem, doc)


def main(doc=None):
    return run_filter(canvas_filter, doc=doc)

if __name__ == '__main__':
    main()
