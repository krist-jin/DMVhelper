# user_data_1 = "TS0141aebd_id=3&TS0141aebd_cr=9c3a2862431f71f9773a47fb4b4d6d4e%3Anmlm%3AA8sUpWQ5%3A1928472670&TS0141aebd_76=0&TS0141aebd_86=0&TS0141aebd_md=2&TS0141aebd_rf=https%3A%2F%2Fwww.dmv.ca.gov%2Fwasapp%2Ffoa%2Fclear.do%3FgoTo%3DdriveTest%26localeName%3Den&TS0141aebd_ct=application%2Fx-www-form-urlencoded&TS0141aebd_pd=numberItems%3D1%26officeId%3D"
user_data_1 = "TS0141aebd_id=3&TS0141aebd_cr=e7a8243dd90001bcb06d4c740c71ece6%3Aeade%3AHrZTAf9e%3A1856281507&TS0141aebd_76=0&TS0141aebd_86=0&TS0141aebd_md=2&TS0141aebd_rf=https%3A%2F%2Fwww.dmv.ca.gov%2Fwasapp%2Ffoa%2Fclear.do%3FgoTo%3DdriveTest%26localeName%3Den&TS0141aebd_ct=application%2Fx-www-form-urlencoded&TS0141aebd_pd=numberItems%3D1%26officeId%3D"
# user_data_2 = "%26requestedTask%3DDT%26firstName%3Dbo%26lastName%3Djin%26dlNumber%3Dy3180379%26birthMonth%3D08%26birthDay%3D17%26birthYear%3D1992%26telArea%3D917%26telPrefix%3D714%26telSuffix%3D4594%26resetCheckFields%3Dtrue"
user_data_2 = "%26requestedTask%3DDT%26firstName%3Ddi%26lastName%3Dli%26dlNumber%3Dy3905569%26birthMonth%3D03%26birthDay%3D19%26birthYear%3D1994%26telArea%3D917%26telPrefix%3D714%26telSuffix%3D4594%26resetCheckFields%3Dtrue"

DMVBody = [
    ("TS0141aebd_id", 3),
    ("TS0141aebd_cr", ""),
    ("TS0141aebd_76", 0),
    ("TS0141aebd_86", 0),
    ("TS0141aebd_md", 2),
    ("TS0141aebd_rf", ""),
    ("TS0141aebd_ct", "application/x-www-form-urlencoded"),
    ("TS0141aebd_pd", "")
]
cr_list = ["e7a8243dd90001bcb06d4c740c71ece6:eade:HrZTAf9e:1856281507", "9c3a2862431f71f9773a47fb4b4d6d4e:nmlm:A8sUpWQ5:1928472670"]
rf_dict = {
    "findDriveTest": "https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do",
    "searchAppts": "https://www.dmv.ca.gov/wasapp/foa/searchAppts.do",
    "reviewDriveTest": "https://www.dmv.ca.gov/wasapp/foa/reviewDriveTest.do"
}
pd_dict = {
    "findDriveTest": "numberItems=1&officeId=%s&requestedTask=DT&firstName=di&lastName=li&dlNumber=y3905569&birthMonth=03&birthDay=19&birthYear=1994&telArea=917&telPrefix=714&telSuffix=4594&resetCheckFields=true",
    "searchAppts": "firstName=di&lastName=li&telArea=917&telPrefix=714&telSuffix=4594"
}

# user_data = "TS0141aebd_id=3&TS0141aebd_cr=e7a8243dd90001bcb06d4c740c71ece6%3Aeade%3AHrZTAf9e%3A1856281507&TS0141aebd_76=0&TS0141aebd_86=0&TS0141aebd_md=2&TS0141aebd_rf=https%3A%2F%2Fwww.dmv.ca.gov%2Fwasapp%2Ffoa%2Fclear.do%3FgoTo%3DdriveTest%26localeName%3Den&TS0141aebd_ct=application%2Fx-www-form-urlencoded&TS0141aebd_pd=numberItems%3D1%26officeId%3D632%26requestedTask%3DDT%26firstName%3Ddi%26lastName%3Dli%26dlNumber%3Dy3905569%26birthMonth%3D03%26birthDay%3D19%26birthYear%3D1994%26telArea%3D917%26telPrefix%3D714%26telSuffix%3D4594%26resetCheckFields%3Dtrue"

searchAppts_body = [
    ("firstName", "Bo"),
    ("lastName", "Jin"),
    ("telArea", "917"),
    ("telPrefix", "714"),
    ("telSuffix", "4594")
]

findDriveTest_body = [
    ("numberItems", "1"),
    ("officeId", ""),
    ("requestedTask", "DT"),
    ("firstName", "bo"),
    ("lastName", "jin"),
    ("dlNumber", "y3180379"),
    ("birthMonth", "08"),
    ("birthDay", "17"),
    ("birthYear", "1992"),
    ("telArea", "917"),
    ("telPrefix", "714"),
    ("telSuffix", "4594"),
    ("resetCheckFields", "true")
]