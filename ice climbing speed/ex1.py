print("Number of competitors:")
num = int(input())
competitors = []
competitors_dict = {}

print("Input competitors info: (as 'BIB No, full name' e.g. 100, Atousa karimi [ENTER])")
for person_idx in range(num):
    bib, competitor = input().split(", ")
    competitors.append([int(bib), competitor])
    competitors_dict[bib] = competitor
print(competitors_dict)

def best_time(results):
    modified_result = results
    for index, result in enumerate(results):
        if result == "Fall":
            modified_result[index] = 1000
        elif result == "Fs":
            modified_result[index] = 2000
        elif result == "DNS":
            modified_result[index] = 3000
        else:
            modified_result[index] = float(result)
    best_result = min(modified_result)
    return best_result

def rank_competitors(comp_times, comp_result):
    final_result = comp_result
    final_time = comp_times
    rank_list = []
    rank = 1
    index = 0
    final_result = sorted(final_result, key=lambda x:x[1])
    final_time = sorted(final_time)

    while index+1 <= num:
        count_time = final_time.count(final_time[index])
        rank_list.extend(count_time*[rank])
        rank += count_time
        index += count_time
    for i in range(num):
        final_result[i].append(rank_list[i])
    return final_result
        

def print_result(sorted_list):
    for item in sorted_list:
        bib = item[0]
        best_record = item[1]
        rank = item[2]
        if best_record == 3000:
            best_record = "DNS"
            rank = "-"
        elif best_record == 2000:
            best_record = "Fs"
        elif best_record == 1000:
            best_record = "Fall"
        print(str(rank)+",", str(bib)+",", competitors_dict.get(str(bib))+",", best_record)
        

print("\nInput competitors results as 'A1 result, A2 result, A3 result' for specified competitor:")
times_list = []
results_list = []
for competitor_idx in range(num):
    bib = competitors[competitor_idx][0]
    print("BIB No.", bib,":")
    times = list(input().split(", "))
    result = best_time(times)
    results_list.append([bib, result])
    times_list.append(result)

print("\nFinal result:", "\n"+30*"-", "\nrank | BIB No. | Name | record", "\n"+15*" -")
print_result(rank_competitors(times_list, results_list))

