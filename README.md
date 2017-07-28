# base64-keystrings.py
## Find key search strings to locate base64-encoded versions of ASCII strings.

*For a detailed breakdown of what this tool is built to accomplish, please see the article on my [blog](https://s7n.co/b64strings)*

When working with obfuscated files (esp. PHP), it's common to find large blocks of base64-encoded code. It's not always possible to programmatically identify, decode, and subsequently test internal base64 blocks when looking for a particular string. This utility can be used to generate the three possible key strings of your intended search pattern (For an explanation of why there are always three strings, where they come from, etc, see my [article](https://s7n.co/b64strings)). Depending on the character count preceding the position of your search term in a file, one of the generated key strings will be present in the base64 block. 

### Usage

```
$ base64-keystrings.py "This is an input string!"
VGhpcyBpcyBhbiBpbnB1dCBzdHJpbmch
aXMgaXMgYW4gaW5wdXQgc3RyaW5n
aGlzIGlzIGFuIGlucHV0IHN0cmlu

$ base64-keystrings.py --file file.txt
VGhpcyBpcyBhIHRleHQgZmls
aXMgaXMgYSB0ZXh0IGZp
aGlzIGlzIGEgdGV4dCBmaWxl

$ cat file.txt | base64-keystrings.py --stdin
VGhpcyBmaWxlIHdhcyBwaXBlZCB0byBzdGRp
aXMgZmlsZSB3YXMgcGlwZWQgdG8gc3RkaW4h
aGlzIGZpbGUgd2FzIHBpcGVkIHRvIHN0ZGlu
```

### Examples

Test to see if a call to "evildomain.com/malware.js" is present in the following obfuscated file:

'''php
<?php
/* 
 * Totally Legit PHP File
 * Version 1.1
 * 
 * Definitely necessary for your website to run. Don't touch it.
 */

 // This file is encoded for copyright protection.
 // Don't decode it or I'll sue you.
 eval(base64_decode(Ly8gSGFoYSB0aGV5J2xsIG5ldmVyIGZpbmQgbWUhCmhhY2tpbmdNYWluZnJhbWUoKTsKaW5qZWN0aW5nQ29kZSgpOwpicm93c2VyVGFrZW92ZXIoJ2h0dHA6Ly9ldmlsZG9tYWluLmNvbS9tYWx3YXJlLmpzJyk7));
'''

'''
$ base64-keystrings.py "evildomain.com/malware.js"
ZXZpbGRvbWFpbi5jb20vbWFsd2FyZS5q
aWxkb21haW4uY29tL21hbHdhcmUu
dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz

$ grep "ZXZpbGRvbWFpbi5jb20vbWFsd2FyZS5q" badfile.txt

$ grep "aWxkb21haW4uY29tL21hbHdhcmUu" badfile.txt

$ grep "dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz" badfile.txt
eval(base64_decode(Ly8gSGFoYSB0aGV5J2xsIG5ldmVyIGZpbmQgbWUhCmhhY2tpbmdNYWluZnJhbWUoKTsKaW5qZWN0aW5nQ29kZSgpOwpicm93c2VyVGFrZW92ZXIoJ2h0dHA6Ly9ldmlsZG9tYWluLmNvbS9tYWx3YXJlLmpzJyk7));
'''

As we can see, the string "dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz" was identified in the file! Applied against a large PHP framework where a code injection could be in a huge assortment of locations, recursive searches could be performed with the generated key strings to assist in locating obfuscated code. 

### Upcoming Features
- [] Add file search features to the script so manual grepping is no longer required