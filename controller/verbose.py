import mechanicalsoup
from datetime import datetime


class VerboseBooster:
    def __init__(self, name, sample_count, res, verbose_input):
        self.name = name
        self.sample_count = sample_count
        self.res = res
        self.students = verbose_input
        self.L1, self.L2, self.L3 = [], [], []
        self.output = []  # 用於存儲輸出文字

    def add_output(self, text):
        self.output.append(text)

    def calculate_study_years(self, enter_year, oral_date):
        try:
            start_date = datetime.strptime(f"{enter_year}/08/01", "%Y/%m/%d")
            oral_date = oral_date.strip().replace("-", "/")
            end_date = datetime.strptime(oral_date, "%Y/%m/%d")
            days_diff = (end_date - start_date).days
            years = round(days_diff / 365, 2)
            return years
        except (ValueError, AttributeError):
            return None

    def show(self):
        try:
            url = 'https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge'
            browser = mechanicalsoup.StatefulBrowser()
            browser.open(url)
            browser.select_form('form[name="main"]')

            browser["qs0"] = self.name
            browser["dcf"] = "ad"
            browser.submit_selected()
            
            ccd = browser.get_url()
            ccd = ccd[52:58:]

            browser.select_form('form[name="main"]')
            browser["sortby"] = "-yr"
            browser["SubmitChangePage"] = "1"

            enter = f"/cgi-bin/gs32/gsweb.cgi/ccd={ccd}/record"
            browser.follow_link(enter.strip())
            now = browser.get_url()
            
            for i in range(1, self.sample_count + 1):
                current_url = now[:69] + str(i)
                browser.open(current_url.strip())
                access = browser.get_current_page()

                try:
                    student_name = access.body.form.div.table.tbody.tr.td.table.find("th", text="研究生:").find_next_sibling().get_text()
                    if student_name in self.students:
                        thesis_title = access.body.form.div.table.tbody.tr.td.table.find("th", text="論文名稱:").find_next_sibling().get_text()
                        grad_year = access.body.form.div.table.tbody.tr.td.table.find("th", text="畢業學年度:").find_next_sibling().get_text()
                        enter_year = int(self.students[student_name][0]) + 1911
                        original_category = self.students[student_name][1]

                        try:
                            oral_defense = access.body.form.div.table.tbody.tr.td.table.find("th", text="口試日期:").find_next_sibling().get_text()
                            study_years = self.calculate_study_years(enter_year, oral_defense)
                        except:
                            oral_defense = "無資料"
                            study_years = None

                        student_data = [
                            f"{str(enter_year)} 年",
                            oral_defense,
                            thesis_title,
                            study_years,
                            grad_year
                        ]

                        if study_years is not None:
                            if study_years <= 2.5:
                                self.L1.append(student_data)
                            elif study_years <= 3.0:
                                self.L2.append(student_data)
                            else:
                                self.L3.append(student_data)
                        else:
                            if original_category == "1":
                                self.L1.append(student_data)
                            elif original_category == "2":
                                self.L2.append(student_data)
                            else:
                                self.L3.append(student_data)
                except Exception as e:
                    continue

            # 生成輸出文字
            self.add_output("\n" + "="*60)
            self.add_output(f"🎓 2.5年(含)以內畢業的 {len(self.L1)} 位學生中：")
            self.add_output("="*60)
            if self.L1:
                for time in self.L1:
                    self.add_output(f"📅 入學時間：{time[0]}")
                    self.add_output(f"🎓 畢業學年度：{time[4]}")
                    self.add_output(f"🎯 口試時間：{time[1]}")
                    self.add_output(f"📚 論文題目：{time[2]}")
                    if time[3] is not None:
                        self.add_output(f"⏱️ 實際就學年數：{time[3]} 年")
                    self.add_output("-"*60)
            else:
                self.add_output("❌ 無資料")
                self.add_output("-"*60)

            self.add_output("\n" + "="*60)
            self.add_output(f"🎓 2.5-3年畢業的 {len(self.L2)} 位學生中：")
            self.add_output("="*60)
            if self.L2:
                for time in self.L2:
                    self.add_output(f"📅 入學時間：{time[0]}")
                    self.add_output(f"🎓 畢業學年度：{time[4]}")
                    self.add_output(f"🎯 口試時間：{time[1]}")
                    self.add_output(f"📚 論文題目：{time[2]}")
                    if time[3] is not None:
                        self.add_output(f"⏱️ 實際就學年數：{time[3]} 年")
                    self.add_output("-"*60)
            else:
                self.add_output("❌ 無資料")
                self.add_output("-"*60)

            self.add_output("\n" + "="*60)
            self.add_output(f"🎓 3年以上畢業的 {len(self.L3)} 位學生中：")
            self.add_output("="*60)
            if self.L3:
                for time in self.L3:
                    self.add_output(f"📅 入學時間：{time[0]}")
                    self.add_output(f"🎓 畢業學年度：{time[4]}")
                    self.add_output(f"🎯 口試時間：{time[1]}")
                    self.add_output(f"📚 論文題目：{time[2]}")
                    if time[3] is not None:
                        self.add_output(f"⏱️ 實際就學年數：{time[3]} 年")
                    self.add_output("-"*60)
            else:
                self.add_output("❌ 無資料")
                self.add_output("-"*60)

            return "\n".join(self.output)

        except Exception as e:
            return f"發生錯誤：{str(e)}"
