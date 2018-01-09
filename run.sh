g++ test.c # compile the code (for now)


# -------------------- TRACING PART ---------------------------------

valgrind -q --tool=callgrind --callgrind-out-file=profile ./a.out > /dev/null

./gprof2dot.py -n0 -e0 --format=callgrind --output=profile.dot profile

python tracer.py | sort -k 2 -r -g > numberOfCalls


#------------------------- REARRANGING PART -------------------


# get the text section of the code
objcopy --dump-section .text=text a.out

# get the function names and starting address
objdump -d -C -j .text a.out | awk '/>:/ {print $1 " " substr($2,2,length($2)-3)}' > functionNames

# get the callsites
objdump -d -C -j .text  a.out | awk '/.*e8.*callq.*/ {print $1 $8}' > calls

# run the rearrangement script
python script.py

# make a new binary with updated text section
objcopy --update-section .text=rearranged_text a.out rearranged_binary 

# run the symbol patcher
./symbol_updater

echo "Done! final_binary created."