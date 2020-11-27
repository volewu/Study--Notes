@restapi.resource('/bu/fixture_management')
class FixtureManagement(Resource):
    def get(self,headers=None):
        BU = request.args.get('BU', '')
        w1 = request.args.get('w1', '')
        w2 = request.args.get('w2', '')

        if w1:
            w1 = int(w1)
            w2 = int(w2)
            how_many_week = w2-w1+1
            station_worktime = 154*how_many_week
            weeklist = []
            weeklist_week = []
            for i in range(w1,w2+1):
                weeklist.append(i)
                weeklist_week.append("'"+'W'+str(i)+"'")
        else:
            how_many_week = 13
            station_worktime = 154*how_many_week
            weeklist=Common.WeekNumList(14)
            weeklist.reverse()
            weeklist = weeklist[:-1]
            weeklist_week = []
            for i in weeklist:
                weeklist_week.append("'"+'W'+str(i)+"'")
        bulist=['MFGI','MFGII','MFGIII','MFGV','MFGVI','MFGVII','MFGVIII','PURE']
        #bulist=['MFGVII']
        result = []
        weeklist_week = (','.join(weeklist_week))
        for bu in bulist:
            bu_totalsn_count = 0
            bu_before_retest_time_count = 0
            bu_retest_time_count = 0
            bu_upgrade_rate = 0
            positive_count = 0
            negative_count = 0
            positive_data = []
            negative_data = []
            fixturelist = []
            data_sql = ''' select * from ICT_Project.uph_performance_detail_all where BU = '{0}' and before_uph != 0 and data_week in ({1}) group by BU,fixture_id,board,data_week'''.format(bu,weeklist_week)
            data = Common.FetchDB(data_sql, BU)
            for row in data:
                if row['BU'] ==bu and row['fixture_id'] not in fixturelist:
                    fixturelist.append(row['fixture_id'])

            for fixture in fixturelist:
                boardlist = []
                fixture_flag = 0
                for row in data:
                    if row['BU'] ==bu and row['fixture_id'] == fixture and row['board'] not in boardlist:
                        boardlist.append(row['board'])

                for board in boardlist:
                    #query = ''' select * from ICT_Project.uph_performance_detail_all where BU = '{0}' and fixture_id = '{1}' and board = '{2}' order by data_week asc '''.format(bu,fixture,board)
                    #rows = Common.FetchDB(query, bu)
                    #before_uph = rows[0]['before_uph']
                    uph_list = [0]*(how_many_week)
                    uph_count = 0
                    uph_num = 0
                    uph_all_num = 0
                    beforeuph = 0
                    upgrade_rate = 0
                    before_retest_time_count = 0
                    retest_time_count = 0
                    uph_avg = 0
                    current_uph = 0
                    a =[]
                    data_list = []
                    for row in data:
                        if row['BU'] ==bu and row['fixture_id'] == fixture and row['board'] == board :
                            data_list.append(row)

                    before_uph = data_list[0]['before_uph']
                    for week in weeklist:
                        for row in data_list:
                            if row['BU'] ==bu and row['fixture_id'] == fixture and row['board'] == board and int(row['data_week'].split('W')[1]) == week :

                                if row['uph'] > 0 :
                                    uph_list[weeklist.index(week)] += row['uph']
                                    uph_count += row['uph']
                                    uph_num += row['uph_num']
                                    uph_all_num += row['uph_num']
                                    before_retest_time_count += row['before_retest_time_count']
                                    retest_time_count += row['retest_time_count']
                                else:
                                    uph_all_num += row['uph_num']


                    if uph_count != 0:
                        uph_list.reverse()
                        uph_avg = round((uph_num/retest_time_count),2)
                        if (before_uph>0):
                            upgrade_rate= round((float(uph_avg)-float(before_uph))/float(before_uph)*100,2)
                        
                        for i in range(len(uph_list)):
                            if uph_list[i] != 0:
                                current_uph = uph_list[i]
                                break
                            else:
                                current_uph = uph_list[i]
                        
                        if upgrade_rate > 0:
                            positive_count += 1
                            positive_data.append({
                                           'BU':bu,
                                           'fixtureid':fixture,
                                           'pn':board,
                                           'current_number':uph_all_num,
                                           'before_uph':before_uph,
                                           'current uph':current_uph,
                                           'upgrade rate':str(upgrade_rate)+'%'
                            })
                        else:
                            negative_count += 1
                            negative_data.append({
                                           'BU':bu,
                                           'fixtureid':fixture,
                                           'pn':board,
                                           'current_number':uph_all_num,
                                           'before_uph':before_uph,
                                           'current uph':current_uph,
                                           'upgrade rate':str(upgrade_rate)+'%'
                            })

                    else:
                        if uph_all_num > 0:
                            uph_avg = 0
                            upgrade_rate= round((float(uph_avg)-float(before_uph))/float(before_uph)*100,2)
                            negative_count += 1
                            negative_data.append({
                                           'BU':bu,
                                           'fixtureid':fixture,
                                           'pn':board,
                                           'current_number':uph_all_num,
                                           'before_uph':before_uph,
                                           'current uph':0,
                                           'upgrade rate':'0%'
                            })
                        else:
                            continue

            positive_rate = positive_count / (positive_count + negative_count)
            negative_rate = 1 - positive_rate
            
            result.append({
                'BU':bu,
                'positive_rate':'%.2f'%(positive_rate*100),
                'negative_rate':'%.2f'%(negative_rate*100),
                'positive_data':positive_data,
                'negative_data':negative_data
            })


        return result