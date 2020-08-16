
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
        self.resources = {'R1':0, 'R2':0, 'R3':0, 'R4':0}
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
            running = process
            process.status = 'running'
            ready_queue.append(process)
        else:
            ready_queue.append(process)
            process.status = 'ready'
    else:
        if running.priority >= process.priority:
            ready_queue.append(process)
            process.status = 'ready'
        else:
            ready_queue.append(process)
            running.status = 'ready'
            running = process
            process.status = 'running'
    # 将进程加入队列并妥善排列
    process_list.append(process)
    sort_queue()
    # 输出
    print('process ' + running.name + ' is running')

# 删除进程
def delete_process(name):
    global running
    global process_list
    global resource_list
    global ready_queue
    global block_queue
    # 停止运行
    if running.name == name:
        running = ''
    # 返还资源
    index = []
    for pro in process_list:
        if pro.name == name:
            for resource in resource_list:
                if pro.resources[resource.name] != 0:
                    index = resource.name
                resource.status += pro.resources[resource.name]
                pro.resources[resource.name] = 0
    # 从队列中删除
    for pro in ready_queue:
        if pro.name == name:
            ready_queue.remove(pro)
    for pro in block_queue:
        if pro.name == name:
            block_queue.remove(pro)
    # 从各资源队列中删除
    for pro in process_list:
        if pro.name == name:
            for resource in resource_list:
                if pro in resource.list:
                    resource.list.remove(pro)
    # 从列表中删除
    for pro in process_list:
        if pro.name == name:
            process_list.remove(pro)
    # 看看能不能唤醒某进程
    process = ''
    for resource in resource_list:
        if resource.name == index:
            if resource.list[0].resources[index] <= resource.status:
                process = resource.list[0]
                # 判断进程状态
                if running == '':
                    if ready_queue == []:
                        running = process
                        process.status = 'running'
                        ready_queue.append(process)
                    else:
                        ready_queue.append(process)
                        process.status = 'ready'
                else:
                    if running.priority >= process.priority:
                        ready_queue.append(process)
                        process.status = 'ready'
                    else:
                        ready_queue.append(process)
                        running.status = 'ready'
                        running = process
                        process.status = 'running'
                # 将进程加入队列并妥善排列
                process_list.append(process)
                sort_queue()
    # 对队列进行排序
    sort_queue()
    # 输出
    if process == '':
        print('release ' + index)
    else:
        print('release ' + index + '. wake up process '+ process.name)

# 展示ready队列
def show_process():
    global ready_queue
    global block_queue
    # 优先级数量初始化
    prior_count = [0, 0, 0]
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

# 展示block的进程
def show_block():
    global resource_list
    for resource in resource_list:
        flag = 0
        print(resource.name + ' ', end = '')
        for pro in resource.list:
            if flag == 0:
                print(pro.name, end='')
            else:
                print('-' + pro.name, end = '')
            flag += 1
        print()

# 请求资源
def request_resouce(name, num):
    global running
    global resource_list
    global ready_queue
    global block_queue
    # 报错
    if running == '':
        print("没有进程运行！")
        return
    for resource in resource_list:
        if resource.name == name:
            # 假如不够分配
            if resource.status < num:
                running.status = 'blocked'
                block_name = running.name
                block_queue.append(running)
                resource.list.append(running)
                running = ready_queue[1]
                ready_queue.pop(0)
                print('process ' + running.name + ' is running.', end = '')
                print('process ' + block_name + ' is blocked.')
            # 假如足够分配
            else:
                running.resources[name] += num
                resource.status -= num
                print('process ' + running.name + ' requests ' + str(num) + ' ' + name)
    sort_queue()

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
        if process.name == running.name:
            ready_queue.append(process)
            ready_name = process.name
    # ready队列头进入running
    if ready_queue[1].name == 'init':
        running = ready_queue[2]
    else:
        running = ready_queue[1]
    ready_queue.pop(0)
    # 重新排序
    sort_queue()
    # 输出
    if running.name == ready_name:
        print('process ' + running.name + ' is running.')
    else:
        print('process ' + running.name + ' is running.', end = '')
        print('process ' + ready_name + ' is ready.')

# 读取文件
def read_file():
    with open('input.txt', 'r') as f:
        for line in f:
            compile(line)

# 对命令处理
def compile(command):
    command = command.split()
    if command[0] == 'read':
        read_file()
    elif command[0] == 'cr':
        create_process(command[1], int(command[2]))
    elif command[0] == 'de':
        delete_process(command[1])
    elif command[0] == 'list' and command[1] == 'ready':
        show_process()
    elif command[0] == 'list' and command[1] == 'block':
        show_block()
    elif command[0] == 'list' and command[1] == 'res':
        show_resource()
    elif command[0] == 'to':
        time_out()
    elif command[0] == 'req':
        request_resouce(command[1], int(command[2]))
    elif command[0] == 'rel':
        release_process_all(command[1])
    elif command[0] == 'ps':
        print_status()
    elif command[0] == 'pr':
        print_resources()

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
    # 读入命令
    while(1):
        print("shell>", end='')
        command = []
        command = input()
        if command.split()[0] == 'read':
            read_file()
        else:
            compile(command)
        
if __name__ == '__main__':
    main()