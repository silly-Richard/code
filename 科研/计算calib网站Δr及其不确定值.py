### 博客文章地址：https://www.cnblogs.com/xzdmlibrary/articles/18348712 ###

from itertools import combinations
import os

def weighted_mean_r(list_1,list_2):
	'''
 	计算weighted mean of ΔR
 	'''
    m_list = []
    n_list = []
    for x,y in zip(list_1,list_2):
        m = x/(y**2)
        n = 1/(y**2)
        m_list.append(m)
        n_list.append(n)
    wmr = sum(m_list)/sum(n_list)
    wmr = round(wmr)
    return wmr

def weighted_uncertainty_mean_r(list_2):
	'''
 	计算weighted uncertainty in mean of ΔR。注意：应当开根号
 	'''
    n_list = []
	for y in list_2:
		n = 1/(y**2)
		n_list.append(n)
	unc_r = (1/sum(n_list))**0.5
	unc_r = round(unc_r)
	return unc_r

def variance_r(list_1,list_2,u):
	'''
 	计算standard deviation of ΔR
 	'''
    m_list = []
    n_list = []
    for x,y in zip(list_1,list_2):
        m = ((x-u)/y)**2
        n = 1/(y**2)
        m_list.append(m)
        n_list.append(n)
    var_r = ((1/(len(list_1)-1))*sum(m_list))/((1/len(list_1))*sum(n_list))
    var_r = var_r**0.5
    var_r = round(var_r)
    return var_r

def check_data(wmr,uncertainty):
	'''
 	确认weighted mean of ΔR和uncertainty值是否是我需要的
 	'''
    if wmr == -76 and uncertainty == 53:
        print('i find result!')
        return 'yes'
    else:
        return 'no'
    
def write_to_txt(txt_name,tups):
	'''
 	将tuple写入txt的
 	'''
    with open(txt_name,'a') as f:
        for tup_num in tups:
            f.write(str(tup_num)+',')
        f.write('\n')
        f.close()

def calcuate(tup_num,way_txt_name):
	'''
 	△R值和不确定值σ的计算函数
 	'''
    r_list = []
    o_list = []

    for num in tup_num:
        r_list.append(r_total[num])
        o_list.append(o_total[num])
    
    wmr = weighted_mean_r(r_list,o_list)
    unc_r = weighted_uncertainty_mean_r(o_list)
    var_r = variance_r(r_list,o_list,wmr)
    uncertainty = max(unc_r,var_r)

    check_result = check_data(wmr=wmr,uncertainty=uncertainty) # 检测计算结果是否是我想要的

    if check_result == 'yes':
        write_to_txt('find.txt',tup_num) # 如果是的，将选择的参照点序列号写入txt文件中保存
    
    write_to_txt(way_txt_name,tup_num) # 将所有参照点的选择结果都写入txt文件中，作为重连的依据

## 脚本主体

# 参照点的△R值和不确定值σ
r_total = [-215,-174,-58,-105,-57,-23,-89,-68,-46,-149,-164,-63,-68,-195,-40,-152,-217,-134,-38,42,-131,-272,-218,-229,-239,-83,-73,-176,-123,-143]
o_total = [50,59,43,41,53,42,35,39,37,40,50,60,70,70,31,40,40,40,45,45,33,35,57,36,44,47,45,41,40,20]

combin_num = 2 # 选取的参照点组合数量

# 选择任意数量ΔR和σ值的组合,不会直接选取,而是通过列表序列号间接选取
num_list = list(range(0,len(r_total)))

# 一级循环,选取任意combin_num数量的ΔR和σ值的组合
while combin_num <= len(r_total):
    
    print(str(combin_num)+' combination is begining!')

	# 二级循环前置,生成存放该次combin_num循环计算结果的txt文件
    way_txt_name = 'way'+str(combin_num)+'.txt'
    dir_list = os.listdir(path=os.getcwd())

	# 二级循环,断线重连机制
    ## 如果该次combin_num循环计算结果的txt文件还未创立,则代表该次循环还未开始
    if way_txt_name not in dir_list:
        f = open(way_txt_name,'w')
        f.close()

		## 对num_list进行匹配,间接对r_total和o_total列表切片
        for tup_num in combinations(num_list,combin_num):
            calcuate(tup_num=tup_num,way_txt_name=way_txt_name)
    
	## 如果该次combin_num循环计算结果的txt文件已经创立,则代表该次循环已经开始
    elif way_txt_name in dir_list:
		## 读取上次计算的保存结果
        f = open(way_txt_name,'r')
		## 获取结果行数,每计算一次,都会将列表的选取结果保存下来的
        lines = len(f.readlines())
        f.close()

		## 判断该次计算结果是否已经计算过,需要跳过的计数变量
        line_num = 1
		
        for tup_num in combinations(num_list,combin_num):
            ## 如果line_num大于lines,说明从这次开始,后面的结果没有计算过
			if line_num > lines:
                calcuate(tup_num=tup_num,way_txt_name=way_txt_name)
            else:
				## 否则pass,line_num自加1,直至大于lines
                print(str(line_num)+' is pass!')
                line_num = line_num + 1
                pass

    combin_num = combin_num +1




