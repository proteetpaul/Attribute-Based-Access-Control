import json

def get_results_rtree(nr):
    range_outfilename = str(nr)+"rectangles_rangeoutput.txt"
    range_outfile = open(range_outfilename, "r")
    range_resfilename = "RangeResults_RTree.txt"
    resfile1 = open(range_resfilename, "a")
    res1 = []
    arr1 = json.load(range_outfile)
    num_points_arr = [0,0,0]
    cnt = [0,0,0]
    time_interval_arr = [0,0,0]
    nodes_arr = [0,0,0]
    for arr in arr1:
        print(len(arr))
        for i in range(0,min(3,len(arr))):
            cnt[i]+=1
            num_points_arr[i] += arr[i][0]
            time_interval_arr[i] += arr[i][1]
            nodes_arr[i] += arr[i][2]
    for i in range(0,3):
        print(i)
        nodes_arr[i] /= cnt[i]
        num_points_arr[i] /= cnt[i]
        time_interval_arr[i] /= cnt[i]
        resfile1.write(str(nodes_arr[i])+' '+str(num_points_arr[i])+' '+str(time_interval_arr[i]))

def get_results_seq_search(nr):
    range_outfilename = str(nr)+"rectangles_RangeSeqSearchOutput.txt"
    range_outfile = open(range_outfilename, "r")
    range_seqresfilename = "RangeSeqSearchResults.txt"
    resfile1 = open(range_seqresfilename, "a")
    res1 = []
    arr1 = json.load(range_outfile)
    num_points_arr = [0,0,0]
    cnt = [0,0,0]
    time_interval_arr = [0,0,0]
    for arr in arr1:
        for i in range(0,min(3,len(arr))):
            cnt[i]+=1
            num_points_arr[i] += arr[i][0]
            time_interval_arr[i] += arr[i][1]
    resfile1.write(str(nr)+" rectangles: \n")
    for i in range(0,3):
        num_points_arr[i] /= cnt[i]
        time_interval_arr[i] /= cnt[i]
        resfile1.write(str(num_points_arr[i])+' '+str(time_interval_arr[i])+'\n')

# r=[1000,5000,10000]
# for x in r:
#     get_results_seq_search(x)