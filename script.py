import subprocess
import tracer

class Function():
    """docstring for Function"""
    def __init__(self, name, calls, text, start_address, length,callSites=[]):
        self.name = name;
        self.calls = calls;
        self.text = text;
        self.startAddress = start_address;
        self.length = length;
        self.callSites = callSites;

class Binary():
    """docstring for Binary"""
    def __init__(self, arr=[],text=None):
        self.arr = arr
        self.text = text;

    def push(self,Function):
        self.arr.append(Function);

class Call(object):
    """docstring for Call"""
    def __init__(self, start, target):
        
        self.start = start
        self.target = target

def readFileHex(fileName):
    with open(fileName, 'rb') as f:
        return f.read().encode('hex');

def readFile(fileName):
    with open(fileName, 'r') as f:
        return f.read();

def initializations(fileName): 
    text = subprocess.call(("objcopy --dump-section .text=text " + fileName).split(" "));
    functionNames = subprocess.call("objdump -d -C -j .text a.out | awk '/>:/' > functionNames".split(" "));
    calls = subprocess.call(["objdump" ,"-d", "-C" ,"-j", ".text", fileName ,"|", "awk", "'/.*e8.*callq.*/ {print $1 $8}'", ">","calls"]);
    if (functionNames != "0"):
        print "Cannot parse function names";
    if (calls != "0"):
        print "Cannot parse callsites";
    

def parse(text, functionNames, callSites,binary,counts):
    # global binary
   
    functionNames = functionNames.strip();
    functionNames = functionNames.split("\n");

    callSites = callSites.strip();
    callSites = callSites.split();
    

    # with open('calls')
    idx = 0;
    tempCalls = 0;
    callIdx = 0;
    for i in xrange(len(functionNames)):
        # print functionNames[i]
        if (len(functionNames[i]) > 0):
            pair = functionNames[i].split(" ");
            address = pair[0];
            # print address
            addressI = int(address,16);
            name = pair[1];
            try:
                pair = functionNames[i+1].split();
                nextAddress = pair[0];
                nextAddressI = int(nextAddress,16);
            except IndexError as e:
                nextAddress = None;

            if (nextAddress is None):
                code = text[idx:];
            else:
                code = text[idx:idx+(nextAddressI-addressI)]

            size = len(code);
            calls = [];
            j = 0;
            for x in range(callIdx, len(callSites)):
                pair = callSites[x].split(":");
                instruction = pair[0];
                target = pair[1];
                # print (int(instruction,16))
                # print addressI
                instructionI = int(instruction,16);
                # print instructionI, addressI, nextAddressI
                if (instructionI >= addressI and instructionI < nextAddressI):
                    # print "SHIT";
                    calls.append(Call(instruction,target));
                    j +=1;
                else:
                    # print "SHIT"
                    break;
            callIdx += j;

            try:
                tempCalls = counts[name];
            except KeyError:
                tempCalls = float("+inf");
            function = Function(name, tempCalls, code, address, size, calls);
            # tempCalls = tempCalls+10;
            print "Parsed function", name;
            binary.push(function);
            idx = idx + len(code);
            # print calls, i

    return binary;

def toFunction(call, function):
    target = int(call.target,16);
    start = int(function.startAddress,16);
    # end = function.startAddress+function.length;
    return (target == start)

# def isNegative(number):


def fixCall(function, callIndex, increment):
    functionStart = int(function.startAddress,16);
    callStart = int(function.callSites[callIndex].start, 16 );

    difference = callStart - functionStart;
    string = function.text[difference:difference+5];
    # print len(string);
    # print len(function.text), function.startAddress, function.callSites[callIndex].start, difference;
    # print callStart, functionStart
    # print function.text;
    # print function.name;

    # print string;
    # print string.encode('hex');
    # string = string.reverse();
    # string = reverse(string);
    string = string[-1::-1];
    # print string;
    # print string.encode('hex')[:-2];
    hexx = string.encode('hex');
    # print int(hexx[:-2],16);
    # print s64(hexx)
    # print string
    # print hexx

    final = hex(int(hexx[:-2], 16) + increment) + "e8";
    final = final[2:]

    # if (len(final) < 10):
    final = "0000000000" + final;
        # print "SHITSHIT SHIT";
    # print final
    # print final

    if (len(final) % 2 == 1):
        final = "0" + final
    final =  final.decode("hex");

    final = final[-1::-1];
    newCall = final[:5];

    text = function.text;

    newText = text[:difference] + newCall + text[difference+5:]
    # print len(text),"->", len(newText)

    function.text = newText;


    # hexx = bin(hexx);

    # bin = bin[2:];
    # if ()
    # summ = bin(int(hexx[:-2],16)) + bin(increment);
    # print int(summ[2:]);

def swap(binary, idx1, idx2):
    print "Swapping", binary.arr[idx1].name, "and", binary.arr[idx2].name;
    temp = binary.arr[idx1];
    binary.arr[idx1] = binary.arr[idx2];
    binary.arr[idx2] = temp;

    calls1 = binary.arr[idx2].callSites;
    start1 = binary.arr[idx2].startAddress;
    length1 = binary.arr[idx2].length;

    calls2 = binary.arr[idx1].callSites;
    start2 = binary.arr[idx1].startAddress;
    length2 = binary.arr[idx1].length;
    
    # fixing callsites in these two functions
    for i in range(len(calls1)):
        if toFunction(calls1[i], binary.arr[idx2]):
            continue;
        elif (not toFunction(calls1[i], binary.arr[idx1])):
            fixCall(binary.arr[idx2], i, -length2);

        else:
            factor = length1 + length2;
            fixCall(binary.arr[idx2], i, -factor);

    for i in range(len(calls2)):
        if toFunction(calls2[i], binary.arr[idx1]):
            continue;
        elif (not toFunction(calls2[i], binary.arr[idx2])):
            fixCall(binary.arr[idx1], i ,length1);

        else:
            factor = length1 + length2;
            fixCall(binary.arr[idx1], i, +factor);            


    for i in range(len(binary.arr)):
        if (i != idx1 and i != idx2):
            calls = binary.arr[i].callSites;

            for j in range(len(calls)):
                if toFunction(calls[j], binary.arr[idx2]):
                    fixCall(binary.arr[i],j,binary.arr[idx1].length);
                    continue;
                elif toFunction(calls[j], binary.arr[idx1]):
                    fixCall(binary.arr[i],j, -binary.arr[idx2].length);


def sort(binary):
    for x in xrange(1, len(binary.arr)):
        for y in xrange(x, 0, -1):
            if binary.arr[y].calls > binary.arr[y-1].calls:
                swap(binary,y-1,y);
                # binary[y], binary[y-1] = binary[y-1], binary[y]

    return binary





if __name__ == '__main__':

    # global binary
    binary = Binary();
    fileName = "a.out";
    # static for now
    # initializations(fileName);
    text = readFile("text");
    functionNames = readFile("functionNames");
    callSites = readFile("calls");
    counts = tracer.parse("profile.dot", fileName);


    print "Beginning parsing"
    binary = parse(text, functionNames, callSites,binary,counts);

    if (len(binary.arr)):
        symbolStart = binary.arr[0].startAddress


    binary = sort(binary);
    # i = 7;

    # print "+============================";
    symbolStart = int(symbolStart,16);
    text = "";

    f=open('rearranged_symbols', 'w');
    for i in range(len(binary.arr)):
        # print binary.arr[i].name;
        # print (binary.arr[i].text.encode("hex"));
        # print binary.arr[i].startAddress
        # print binary.arr[i].length;
        # print binary.arr[i].callSites;
        f.write(hex(symbolStart) + " "+ binary.arr[i].name+"\n");
        symbolStart += binary.arr[i].length;

        text = text + binary.arr[i].text;

    print "Written rearranged_symbols";
    print "Generating rearranged text section"
    f.close();
    f=open('rearranged_text','w');
    f.write(text);
    f.close();
    print "Written rearranged_text";
    # print text;



    # fixCall(binary.arr[7],1, +45);