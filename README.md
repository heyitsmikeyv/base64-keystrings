# base64-keystrings.py
## Find key search strings to locate base64-encoded versions of ASCII strings.

*For a detailed breakdown of what this tool is built to accomplish, please see the article on my [blog](https://michaelveenstra.com/2017/07/27/searching-for-phrases-in-base64-encoded-strings/)*

When working with obfuscated files (esp. PHP), it's common to find large blocks of base64-encoded code. It's not always possible to programmatically identify, decode, and subsequently test internal base64 blocks when looking for a particular string. This utility can be used to generate the three possible key strings of your intended search pattern (For an explanation of why there are always three strings, where they come from, etc, see my [article](https://michaelveenstra.com/2017/07/27/searching-for-phrases-in-base64-encoded-strings/)). Depending on the character count preceding the position of your search term in a file, one of the generated key strings will be present in the base64 block. 

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

We can use it to tackle an example problem: Finding a string in an obfuscated PHP file.

Our company's imaginary website is serving malicious javascript to our users! The script is being sourced from evildomain.com/malware.js. We're running a pretty big framework so it's not trivial to identify the file it's coming from, and searching our files for that address turned up empty. Let's see if it's been base64-encoded.

```
$ base64-keystrings.py "evildomain.com/malware.js" 
ZXZpbGRvbWFpbi5jb20vbWFsd2FyZS5q 
aWxkb21haW4uY29tL21hbHdhcmUu 
dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz 

$ grep -ro -e "ZXZpbGRvbWFpbi5jb20vbWFsd2FyZS5q" -e "aWxkb21haW4uY29tL21hbHdhcmUu" -e "dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz" public_html/
./public_html/includes/media/badfile.php:dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz 
```

Searching for our three key strings in public_html/ turned up the culprit: ./public_html/includes/media/badfile.php!

```php
<?php
/* 
 * badfile.php
 * Totally Legit PHP File
 * Version 1.1
 * 
 * Definitely necessary for your website to run. Don't touch it.
 */

 // This file is encoded for copyright protection.
 // Don't decode it or I'll sue you.
 eval(base64_decode("Ly8gSGFoYSB0aGV5J2xsIG5ldmVyIGZpbmQgbWUhCmhhY2tpbmdNYWluZnJhbWUoKTsKaW5qZWN0aW5nQ29kZSgpOwpicm93c2VyVGFrZW92ZXIoJ2h0dHA6Ly9ldmlsZG9tYWluLmNvbS9tYWx3YXJlLmpzJyk7"));
```

As we can see, the string "dmlsZG9tYWluLmNvbS9tYWx3YXJlLmpz" was identified in the file.

### Upcoming Features
- [ ] Add file search features to the script so manual grepping is no longer required
- [ ] Add a flag to generate additional key strings for rot13, strrev, etc.
