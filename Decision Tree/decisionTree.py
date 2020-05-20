import sys
import csv
class Node:
    def __init__(self,splitted_att = None, peer = None, left = None,right = None):
        self.splitted_att = splitted_att
        self.peer = peer
        self.left= left
        self.right = right
class Tree:
    def __init__(self):
        self.root = Node()
        self.root.splitted_att = -1
        self.Attributes = None
        self.attributeNames = None
        self.lines = None
    def openFile(self, filename):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            line_count = 0
            lines = []
            self.attributeNames = []
            self.Attributes = []
            for i in range(0, 20):
                self.Attributes.append(i)
            for row in csv_reader:
                if line_count == 0:
                    for i in range(len(row)-1):
                        self.attributeNames.append(row[i])
                    line_count += 1
                else:
                    lines.append(row)
                    line_count += 1

        return lines
    def build(self, datas,type):
        if len(datas) == 0:
            self.root = None
        else:
            if(type == 'g'):
                self.root = self.splitting(datas, self.Attributes,'g')
            elif (type == 'i'):
                self.root = self.splitting(datas, self.Attributes,'i')
    def splitting(self, datas, Attributes, types):
        root = Node()
        onesNum = 0
        zerosNum = 0
        for i in range(len(datas)):
            if (datas[i][20] == '1'):
                onesNum += 1
            else:
                zerosNum += 1
        if onesNum > zerosNum:
            root.peer = '1'
        else:
            root.peer = '0'
        if types == 'g':
            splitted_point_info = self.splitted_point_info(datas, Attributes)
            splitpoint = splitted_point_info[0]
            if len(Attributes) == 0 or splitpoint == -1:
                return root
            root.splitted_att = splitpoint
            newAttributes = []
            for attribute in Attributes:
                if attribute != splitpoint:
                    newAttributes.append(attribute)
            Attributes = newAttributes
            root.left = self.splitting(splitted_point_info[1], Attributes,'g')
            root.right = self.splitting(splitted_point_info[2], Attributes,'g')
        elif types == 'i':
            splitpoint_info = self.impurity_splitted_info(datas, Attributes)
            splitpoint = splitpoint_info[0]
            if len(Attributes) == 0 or splitpoint == -1:
                return root

            root.splitted_att = splitpoint
            newAttributes = []
            for attribute in Attributes:
                if attribute != splitpoint:
                    newAttributes.append(attribute)
            Attributes = newAttributes
            root.left = self.splitting(splitpoint_info[1], Attributes,'g')
            root.right = self.splitting(splitpoint_info[2], Attributes,'g')
        return root
    def splitted_point_info(self,datas, Attributes):
        temp = 0
        dataset1 = []
        dataset0 = []
        split_attribute = -1
        for attribute in Attributes:
            dataset3 = []
            dataset4 = []
            for i in range(len(datas)):
                if (datas[i][attribute] == '1'):
                    dataset3.append(datas[i])
                if (datas[i][attribute] == '0'):
                    dataset4.append(datas[i])
            onesNum = 0
            zerosNum = 0
            totalNum = 0
            for i in range(len(datas)):
                if (datas[i][20] == '1'):
                    onesNum += 1
                    totalNum += 1
                else:
                    zerosNum += 1
                    totalNum += 1
            if (zerosNum == 0 or onesNum == 0):
                data_entropy1 = 0
            else:
                data_entropy1 = (zerosNum / totalNum) * (onesNum / totalNum)
            onesNum = 0
            zerosNum = 0
            totalNum = 0
            for i in range(len(dataset4)):
                if (dataset4[i][20] == '1'):
                    onesNum += 1
                    totalNum += 1
                else:
                    zerosNum += 1
                    totalNum += 1
            if (zerosNum == 0 or onesNum == 0):
                data_entropy2 = 0
            else:
                data_entropy2 = (zerosNum / totalNum) * (onesNum / totalNum)
            onesNum = 0
            zerosNum = 0
            totalNum = 0
            for i in range(len(dataset3)):
                if (dataset3[i][20] == '1'):
                    onesNum += 1
                    totalNum += 1
                else:
                    zerosNum += 1
                    totalNum += 1
            if (zerosNum == 0 or onesNum == 0):
                data_entropy3 = 0
            else:
                data_entropy3 = (zerosNum / totalNum) * (onesNum / totalNum)
            gain = data_entropy1 - (len(dataset4) * data_entropy2 / len(datas) + len(dataset3) * data_entropy3 / len(datas))
            if(gain > temp):
                temp = gain
                split_attribute = attribute
                dataset0 = dataset4
                dataset1 = dataset3
        return split_attribute,dataset0,dataset1
    def impurity_splitted_info(self, datas, Attributes):
        maxgain = 0
        dataset1 = []
        dataset0 = []
        split_attribute = -1
        for attribute in Attributes:
            info = self.impurity_gain(datas, attribute)
            if (info[0] != 0 and info[0]>maxgain):
                maxgain = info[0]
                split_attribute = attribute
                dataset0 = info[1]
                dataset1 = info[2]
        return split_attribute, dataset0, dataset1
    def impurity_gain(self, datas, attribute):
        ones = []
        zeros = []
        total = len(datas)
        for i in range(len(datas)):
            if (datas[i][attribute] == '1'):
                ones.append(datas[i])
            if (datas[i][attribute] == '0'):
                zeros.append(datas[i])
        if (len(zeros)==0 or len(ones)==0):
            return 0, zeros, ones
        else:
            gain = self.impurity(datas)-((len(zeros)/total * self.impurity(zeros))+(len(ones)/total * self.impurity(ones)))
        return gain, zeros, ones
    def impurity(self, datas):
        onesNum = 0
        zerosNum = 0
        totalNum = 0
        for i in range(len(datas)):
            if (datas[i][20] == '1'):
                onesNum += 1
                totalNum += 1
            else:
                zerosNum += 1
                totalNum += 1
            if zerosNum == 0 or onesNum == 0:
                impurity = 0
            else:
                impurity = (onesNum/totalNum)*(zerosNum*totalNum)
        return impurity
    def print_tree(self, node, depth, attributeNames):
        tree = ''
        sign = ''
        if node is None:
            return ' '
        if node.left is None and node.right is None:
            tree = tree + str(node.peer) + '\n'
            return tree
        for i in range(depth):
            sign = sign + '| '
        tree = tree + sign
        temp = attributeNames[node.splitted_att]
        if node.left.left is None and node.left.right is None:
            tree = tree + temp + "=0:"
            tree = tree + self.print_tree(node.left, depth + 1, attributeNames)
            tree = tree + sign
        else:
            tree = tree + temp + "=0:\n"
            tree = tree + self.print_tree(node.left, depth + 1, attributeNames)
            tree = tree + sign

        if node.right.right is None and node.right.left is None:
            tree = tree + temp + "=1:"
            tree = tree + self.print_tree(node.right, depth + 1, attributeNames)
        else:
            tree = tree + temp + "=1:\n"
            tree = tree + self.print_tree(node.right, depth + 1, attributeNames)

        return tree
    def Accuracy(self, root, filename):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter= ',')
            line_count = 0
            lines = []
            self.attributeNames = []
            self.Attributes = []
            for i in range(0, 20):
                self.Attributes.append(i)
            for row in csv_reader:
                if line_count == 0:
                    for i in range(len(row)-1):
                        self.attributeNames.append(row[i])
                    line_count += 1
                else:
                    lines.append(row)
                    line_count += 1
        self.lines = lines
        if root == None or len(self.lines) == 0:
            return 0
        match = 0
        for i in range(len(self.lines)):
            matched = self.matched_value(root, self.lines[i])
            if matched == self.lines[i][20]:
                match += 1
        self.accuracy = match / len(self.lines)
        return self.accuracy
    def matched_value(self, root, row):
        if root.splitted_att == None:
            return root.peer
        if row[root.splitted_att] == '1':
            return self.matched_value(root.right, row)
        else:
            return self.matched_value(root.left, row)
def main(argv):

    training_set = sys.argv[1]
    validation_set = sys.argv[2]
    test_set = sys.argv[3]
    to_print = sys.argv[4]
    heuristic = sys.argv[5]

    treeGain = Tree()
    treeImpurity = Tree()
    accuracy = Tree()
    accuracy1 = Tree()
    accuracy2 = Tree()

    training_data1 = treeGain.openFile(training_set)
    treeGain.build(training_data1,'g')

    training_data2 = treeImpurity.openFile(training_set)
    treeImpurity.build(training_data2,'i')


    if heuristic == 'gain':
        if to_print == 'yes':
            print('Using information gain heuristic for training:\n',treeGain.print_tree(treeGain.root, 0, treeGain.attributeNames))
        print('Accuracy for gain algorithm for training:', accuracy.Accuracy(treeGain.root, training_set))
        print('Accuracy for gain algorithm for validation:',accuracy1.Accuracy(treeGain.root,validation_set))
        print('Accuracy for gain algorithm for test:',accuracy2.Accuracy(treeGain.root,test_set))
    if heuristic == 'variance':
        if to_print == 'yes':
            print('Using variance impurity heuristic for training:\n',treeImpurity.print_tree(treeImpurity.root, 0, treeImpurity.attributeNames))
        print('Accuracy for variance impurity algorithm for training:',accuracy.Accuracy(treeImpurity.root,training_set))
        print('Accuracy for variance impurity algorithm for validation:',accuracy1.Accuracy(treeImpurity.root,validation_set))
        print('Accuracy for variance impurity algorithm for test:',accuracy2.Accuracy(treeImpurity.root,test_set))

if __name__ == "__main__":
    main(sys.argv)
