#!/usr/bin/env python3

# (c) 2021 probonopd
# Python port of https://github.com/jackyf/so-stub/blob/master/so-stub by jackyf
# NOT WORKING YET, CONTRIBUTIONS WELCOME
#
# MIT License

import sys, os, re
import fileinput, subprocess, inspect

def process_symbol_table(path, mode, callback):
   print("Reading symbol table of %s ..." % path)

   nm_opt_args = '--defined-only --print-size'
   symbol_table = subprocess.run(["nm", path, "--dynamic", nm_opt_args], capture_output=True, text=True).stdout
   
   lines = symbol_table.split('\n')

   for line in lines:
      line = line.rstrip("\n")
      parts = re.split(' ', line)
      print(line)
      # FIXME: if mode == 'caller' or(():

def process_ldd(main_caller_path, lib_prefix):

   print("Processing dynamic dependencies of %s ..." % main_caller_path)
   caller_ldd_output = subprocess.run(["ldd", main_caller_path], capture_output=True, text=True).stdout
   
   # print(caller_ldd_output)
   
   # FIXME: Properly translate to Python
   # if(default_match: = re.match(re.compile($lib_prefix[^ ]*)  = > (.*?) , re.I), caller_ldd_ouptut)):
   #    print("could not find {lib_prefix} in dynamic dependencies for {main_caller_path}")
   # lib_file = default_match.group(1)
   # lib_path = default_match.group(2)
   #
   # all_callers = ((default_match: = re.match(re.compile(' = > (.*?) ', re.G), caller_ldd_ouptut)))
   # main_caller_path
   # all_callers = filter default_var != lib_path all_callers
   #
   # return lib_path, all_callers

def get_lib_id(arg_array):
   result = arg_array[0]
   result = str.replace('\.so.*', '\.so.*') # FIXME: This is probably wrong
   result = str.replace('[^0-9a-z]+', '[^0-9a-z]+') # FIXME: This is probably wrong
   return(result)

if len(sys.argv) != 4:
    print("USAGE: %s caller so lang" % sys.argv[0])
    print("    caller: full path to an executable or a shared library which uses so (directly or indirectly);")
    print("    so: shared library (.so) to stub; can be a full library file name or a distinguishable prefix;")
    print("    lang: either c or cpp.")
    exit(1)

[argv0, main_caller_path, lib_prefix, lang] = sys.argv

if lang != 'cpp' and lang != 'c':
   print("invalid language %s" % lang)
   exit(1)

[lib_path, all_callers] = process_ldd(main_caller_path, lib_prefix)
output_file = basename(lib_path)
lib_id = get_lib_id([output_file])

print("Will create a stub library for %s (%s) used in %s" % (lib_id, output_file, main_caller_path))

caller_symbol_set = None

for caller_path in all_callers:
   process_symbol_table(caller_path, 'caller')
   symbol = caller_path[0]
   caller_symbol_set[symbol] = 1

used_symbols = None
unused_symbol_count = 0
process_symbol_table(lib_path, 'lib')

for process_symbol in process_symbol_table:
    symbol = process_symbol[0]
    if caller_symbol_set  !=  none:
        used_symbols.append(symbol)

if used_symbol_count == 0:
    print("no used symbols found, stub library will be empty")

print("Output file: %s" % output_file)

function_name = "so_stub_for_%s" % lib_id
print("Stub function name: %s" % function_name)

output_path = output_file

if lang == 'cpp':
   print("Using C++ stubs - library function stubs will throw std::runtime_error")
   print("  -> catch this exception in the code to make the library optional")
elif lang == 'c':
   print("Using C stubs - library function stubs will call abort()")
   print("  -> check for environment variable '{function_name}' before using the library")

print("Compiling ...")

for sym in used_symbols:
   print("-Wl, --defsym = %s = %s" % (sym, function_name)) # FIXME: Write to temporary file
   
defines = '-DLNAME = \\\"%s\\\" -DFNAME = %s' % (output_file, function_name)
if os.system("g++ -shared -Wall -fPIC %s stubs.%s \@%s -o %s" % (defines, lang, defsym_args_file, output_path)) == 0:
   print("compiling failed: %s" % unix_diag_message)

print("Stripping ...")

if os.system("strip %s" % output_path) == 0:
   print("strip failed: %s" % unix_diag_message)

print("Done")
