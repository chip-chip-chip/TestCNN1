import torch
from torch.utils.data import DataLoader
from torch import nn, optim

from lenet5 import Lenet5
from dataset import ReadData

# 主函数
def main():
    batchsz = 5 # batchsz 大小为5
    logo_train = ReadData(train=True)  # 获得训练集
    # 加载训练集为DataLoader
    logo_train = DataLoader(logo_train, batch_size=batchsz, shuffle=True)
    # 获得测试集
    logo_test = ReadData(train=False)
    logo_test = DataLoader(logo_test, batch_size=batchsz, shuffle=True)

    x, label = iter(logo_train).next()
    print('x:', x.shape, 'label:', label.shape)

    device = torch.device('cuda') # cuda
    # model = Lenet5().to(device) # 使用cuda
    model = Lenet5() # 实例化模型

    # criteon = nn.CrossEntropyLoss().to(device) # 使用cuda
    criteon = nn.CrossEntropyLoss()  # 不使用cuda
    # 优化器
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    print(model) # 打印模型
    for epoch in range(100):
        # 训练
        model.train()
        for batchidx, (x, label) in enumerate(logo_train):
            # [b, 3, 32, 32]
            # [b]
            # x, label = x.to(device), label.to(device)
            logits = model(x)
            # logits: [b, 10]
            # label:  [b]
            # loss: tensor scalar
            loss = criteon(logits, label) # 计算损失率
            # backprop
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # 进行预测,计算准确度
        model.eval()
        with torch.no_grad():
            #test
            total_correct = 0
            total_num = 0
            for x, label in logo_test:
                # [b, 3, 32, 32]
                # [b]
                # x, label = x.to(device), label.to(device)
                # [b, 10]
                logits = model(x)
                # [b]
                pred = logits.argmax(dim=1)
                # [b] vs [b] => scalar tensor
                # print('预测:',torch.max(logits,1)[1].data.numpy(), "实际", label[:batchsz].numpy())
                correct = torch.eq(pred, label).float().sum().item()
                total_correct += correct
                total_num += x.size(0)
                # print(correct)
            acc = total_correct / total_num
            print('epoch:',epoch, 'acc:', acc)
            if epoch%10 == 0:
                save_path = "./model/"+str(epoch)+"_model.plk"
                torch.save(model,save_path)  # 保存模型
                print("保存模型成功")
    # 保存最后的模型
    last_model = "./model/last_model.plk"
    torch.save(model, last_model)

if __name__ == '__main__':
    main()
