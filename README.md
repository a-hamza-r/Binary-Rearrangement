# Binary-Rearrangement
Rearranging a binary to reduce the execution time

## Description
The primary goal is to place the frequently used functions first in any ELF format executable binary. Whenever such a function needs to be run, it will most probably be available in the memory due to the rearrangement, leading to reduced page faults because the function would not be needed to loaded in the memory as it will already be present there. This will consequently reduce the execution time. The program rearranges the binary according to the frequency of each function called in the binary.

## How to run
Run the "run.sh" file provided. It has all the necessary commands to run the project. After the rearranging has been done, the new binary is "final_binary". 