from controller import lab_census_system
from controller import verbose

if __name__=="__main__":
    # handle user input
    school = input('欲查詢學校[1.交大 2.中央 3.清大]，輸入數字：')
    name = input('教授名稱：')
    sample_count = int(input('參考最近碩士畢業生的數量：'))
    filter_cnt = input('欲過濾的系所數量（選填）：')

    LCS = lab_census_system.LabCensusSystem(school, name, sample_count, filter_cnt)
    verbose_input = LCS.Search()
    res = LCS.Show()
    print(f"最近 {str(sample_count)} 筆碩士畢業生紀錄中")
    print(f"{res[0]}\t位2年左右畢業")
    print(f"{res[1]}\t位2-3年畢業")
    print(f"{res[2]}\t位3年以上畢業")

    V = verbose.VerboseBooster(name, sample_count, res, verbose_input)
    V.show()
