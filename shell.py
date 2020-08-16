
# 进程列表
process_list = []
# 资源列表
resource_list = []
# 进程队列
ready_queue = []
block_queue = []
# 正在运行的进程
running = ''

# 进程控制块
class Pcb:
    def __init__(self, name = '', priority = 0):
        self.name = name
        self.CPU_state = False
        self.Memory = False
        self.Open_files = False
        self.resources = [0, 0, 0, 0]
        self.status = ''
        self.list = []
        self.tree = ''
        self.priority = priority

# 资源控制块
class Rcb:
    def __init__(self, name = '', status = 0):
        self.name = name
        self.status = status 
        self.list = []

# 创建进程
def create_process(name, priority):
    global process_list
    global ready_queue
    global running
    # 名称是否重复
    for pro in process_list:
        if pro.name == name:
            print("名字重复了")
            return
    # 进程初始化
    process = Pcb(name, priority)
    # 判断进程状态
    if running == '':
        if ready_queue == []:
            running = process.name
            process.status = 'running'
        else:
            ready_queue.append(process)
            process.status = 'ready'
    else:
        ready_queue.append(process)
        process.status = 'ready'
    # 将进程加入队列并妥善排列
    process_list.append(process)
    sort_queue()

# 删除进程
def delete_process(name):
    global running
    global process_list
    global resource_list
    global ready_queue
    global block_queue
    # 停止运行
    if running == name:
        running = ''
    # 返还资源
    for pro in process_list:
        if pro.name == name:
            for i in range(len(resource_list)):
                resource_list[i].status += pro.resources[i]
                pro.resources[i] = 0
    # 从队列中删除
    for pro in ready_queue:
        if pro.name == name:
            ready_queue.remove(pro)
    for pro in block_queue:
        if pro.name == name:
            block_queue.remove(pro)
    # 从列表中删除
    for pro in process_list:
        if pro.name == name:
            process_list.remove(pro)
    # 对队列进行排序
    sort_queue()

# 展示队列队列
def show_process(type = 'ready'):
    global ready_queue
    global block_queue
    # 优先级数量初始化
    prior_count = [0, 0, 0]
    if type == 'ready':
        # 统计各个优先级数量
        for pro in ready_queue:
            if pro.priority == 0:
                prior_count[0] += 1
            elif pro.priority == 1:
                prior_count[1] += 1
            elif pro.priority == 2:
                prior_count[2] += 1
        for i in reversed(range(3)):
            flag = 0
            print(str(i) + ':', end = '')
            for pro in ready_queue:
                if pro.priority == i:
                    if flag == 0:
                        print(pro.name, end='')
                    else:
                        print('-' + pro.name, end='')
                    flag += 1
            print()
    if type == 'block':
        # 统计各个优先级数量
        for pro in block_queue:
            if pro.priority == 0:
                prior_count[0] += 1
            elif pro.priority == 1:
                prior_count[1] += 1
            elif pro.priority == 2:
                prior_count[2] += 1
        for i in reversed(range(3)):
            flag = 0
            print(str(i) + ':', end = '')
            for pro in block_queue:
                if pro.priority == i:
                    if flag == 0:
                        print(pro.name, end='')
                    else:
                        print('-' + pro.name, end='')
                    flag += 1
            print()

# 展示资源
def show_resource():
    global resource_list
    for resource in resource_list:
        print(resource.name + ' ' + str(resource.status))

# 模拟时钟中断
def time_out():
    global ready_queue
    global running
    # 运行中的加入ready队列
    for process in process_list:
        if process.name == running:
            ready_queue.append(process)
    # ready队列头进入running
    running = ready_queue[0].name
    ready_queue.pop(0)
    # 重新排序
    sort_queue()

# 排列队列
def sort_queue():
    global ready_queue
    global block_queue
    # 排列ready队列
    tmp_1 = []
    for pro in ready_queue:
        if pro.priority == 2:
            tmp_1.append(pro)
    for pro in ready_queue:
        if pro.priority == 1:
            tmp_1.append(pro)
    for pro in ready_queue:
        if pro.priority == 0:
            tmp_1.append(pro)
    ready_queue = tmp_1
    # 排列block队列
    tmp_2 = []
    for pro in block_queue:
        if pro.priority == 3:
            tmp_2.append(pro)
    for pro in block_queue:
        if pro.priority == 2:
            tmp_2.append(pro)
    for pro in block_queue:
        if pro.priority == 1:
            tmp_2.append(pro)
    block_queue = tmp_2
    


def main():
    global process_list
    global resource_list
    global ready_queue
    global block_queue
    global running
    # 初始化资源和PCB
    pcb = create_process('init', 0)
    r1 = Rcb('R1', 1)
    r2 = Rcb('R2', 2)
    r3 = Rcb('R3', 3)
    r4 = Rcb('R4', 4)
    # 将进程和资源加入全局变量
    resource_list.append(r1)
    resource_list.append(r2)
    resource_list.append(r3)
    resource_list.append(r4)
    # 打印初始化结果
    print("Process init is done.")
    # 读入命令
    while(1):
        print("shell>", end='')
        command = []
        command = input().split()
        if command[0] == 'read':
            read_file()
        elif command[0] == 'cr':
            create_process(command[1], int(command[2]))
        elif command[0] == 'de':
            delete_process(command[1])
        elif command[0] == 'list' and command[1] == 'ready':
            show_process('ready')
        elif command[0] == 'list' and command[1] == 'block':
            show_process('block')
        elif command[0] == 'list' and command[1] == 'res':
            show_resource()
        elif command[0] == 'to':
            time_out()
        elif command[0] == 'rel':
            release_process_all(command[1])
        elif command[0] == 'ps':
            print_status()
        elif command[0] == 'req':
            request_resouce(command[1], command[2])
        elif command[0] == 'pr':
            print_resources()
        

if __name__ == '__main__':
    main()