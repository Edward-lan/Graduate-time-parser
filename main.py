from controller import lab_census_system
from controller import verbose

def validate_school_input(school):
    try:
        school = str(school).strip()
        valid_schools = {'1', '2', '3'}
        if school not in valid_schools:
            raise ValueError('無效的學校代碼')
        return school
    except Exception:
        raise ValueError('請輸入有效的學校代碼')

def validate_sample_count(input_str):
    try:
        count = int(input_str)
        if count <= 0:
            raise ValueError('請輸入大於0的數字')
        return count
    except ValueError:
        raise ValueError('請輸入有效的數字')

def validate_filter_count(input_str):
    if not input_str:
        return 0
    try:
        return int(input_str)
    except ValueError:
        print('警告：過濾系所數量無效，將使用預設值0')
        return 0

if __name__=="__main__":
    try:
        # 處理使用者輸入
        school = validate_school_input(input('欲查詢學校[1.交大 2.中央 3.清大]，輸入數字：'))
        name = input('教授名稱：').strip()
        while not name:
            print('錯誤：教授名稱不能為空')
            name = input('教授名稱：').strip()
            
        sample_count = validate_sample_count(input('參考最近碩士畢業生的數量：'))
        filter_cnt = validate_filter_count(input('欲過濾的系所數量（選填）：'))

        # 建立查詢系統並執行
        LCS = lab_census_system.LabCensusSystem(school, name, sample_count, filter_cnt)
        verbose_input = LCS.Search()
        res = LCS.Show()

        # 顯示結果
        print(f"\n查詢結果：")
        print(f"最近 {str(sample_count)} 筆碩士畢業生紀錄中")
        print(f"{res[0]}\t位2年左右畢業")
        print(f"{res[1]}\t位2-3年畢業")
        print(f"{res[2]}\t位3年以上畢業")

        # 顯示詳細資訊
        V = verbose.VerboseBooster(name, sample_count, res, verbose_input)
        V.show()

    except Exception as e:
        print(f"\n發生錯誤：{str(e)}")
        print("請確認輸入資料是否正確，或聯繫系統管理員")
