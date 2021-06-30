from collections import Counter, defaultdict


def WAND_Algo(query_terms, top_k, inverted_index):
    terms_U = defaultdict(int)
    posting = defaultdict(int)
    set_terms = defaultdict(list)
    set_dict = defaultdict(list)
    valid_parameter = 0
    for t in range(len(query_terms)):
        terms_U[t] = 0
        posting[t] = 0
        copy_eachterm_lsit = list(inverted_index[query_terms[t]])
        if len(copy_eachterm_lsit) == 0:
            continue
        copy_eachterm_lsit.append((3001, -1))  # add the end symbol to each list [(1, 4), (2, 4), (3, 4),(0,0)]
        set_terms[t] = copy_eachterm_lsit  # we move the position in this set, and this set save the list of each term
        set_dict[t] = inverted_index[query_terms[t]][posting[t]]
        if inverted_index[query_terms[t]][posting[t]][0] != 3001:
            valid_parameter += 1
        for i in copy_eachterm_lsit:
            if i[-1] > terms_U[t]:
                terms_U[t] = i[-1]  # set each term's Upperbound, save in  terms_U, the keys are terms(str)
    theta = -99
    Ans = []
    sorted_dict = sorted(set_dict.items(), key=lambda x: x[0])
    full_evaluation = 0
    while valid_parameter > 0:  # if the candidate number is not zero
        sorted_dict = sorted(sorted_dict, key=lambda x: x[1][0])  # sort the dict based on the docID
        score_limit = 0
        pivot = 0
        while pivot < len(sorted_dict) - 1:
            tmp_s_lim = score_limit + terms_U[sorted_dict[pivot][0]]
            if tmp_s_lim > theta:
                break
            score_limit = tmp_s_lim
            pivot += 1
        pivot_docID = sorted_dict[pivot][1][0]
        if pivot == len(sorted_dict) - 1:
            score_limit = score_limit + terms_U[sorted_dict[pivot][0]]
            if score_limit <= theta:
                break
        if pivot_docID == 3001:
            break
        if sorted_dict[0][1][0] == pivot_docID:  # if the first docID in the sorted terms is equal to pivotID
            s = 0
            t = 0
            while t < len(set_dict) and sorted_dict[t][1][0] == pivot_docID:
                s = s + sorted_dict[t][1][1]
                posting[sorted_dict[t][0]] += 1
                sorted_dict[t] = (
                sorted_dict[t][0], set_terms[sorted_dict[t][0]][posting[sorted_dict[t][0]]])  # update the
                if set_terms[sorted_dict[t][0]][posting[sorted_dict[t][0]]][0] == 3001:  # pointer
                    valid_parameter -= 1
                t += 1
            full_evaluation += 1
            if s > theta:
                Ans.append((s, pivot_docID))
                sorted_Ans = sorted(Ans, key=lambda x: x[0], reverse=True)
                Ans = sorted_Ans
                if len(Ans) > top_k:
                    Ans.pop()
                    theta = Ans[-1][0]
        else:
            for t in range(pivot):
                target_doc = pivot_docID  # set the target docID
                for position in range(
                        len(set_terms[sorted_dict[t][0]])):  # find the docID which is larger or equal than target id
                    if set_terms[sorted_dict[t][0]][position][0] >= target_doc:
                        posting[sorted_dict[t][0]] = position
                        sorted_dict[t] = (sorted_dict[t][0], set_terms[sorted_dict[t][0]][posting[sorted_dict[t][0]]])
                        if sorted_dict[t][1][0] == 3001:
                            valid_parameter -= 1
                        break
    return Ans, full_evaluation
