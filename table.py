
# TODO ANALISAR PDF INTEIRO E PEGAR PALAVRAS SEPARADAS POR ESPACAMENTO DA AREA CADA PALAVRA UMA COLUNA
class Table:
    def __init__(self, data, selecteda=[]):
        self.data = data
        self.selecteda = selecteda

    def rows(self):
        rows = self.data.split('\n')
        return rows

    def words(self):
        words = []
        for row in self.rows():
            words += row.split('  ')
            words[:] = [x.strip() for x in words if x]
        return words

    def wordsPosition(self):
        wordPosition = []
        for y, row in enumerate(self.rows()):
            newRow = row
            wordsRow = row.split('  ')
            wordsRow[:] = [x.strip() for x in wordsRow if x]
            for word in wordsRow:          
                wordPosition.append([word, newRow.find(word), y])
                newRow = newRow.replace(word, " "*len(word), 1)
        return wordPosition

    def centerColumns(self, variance):
        positions = [0]
        for word in self.wordsPosition():
            add = True
            for position in positions:
                if(word[1] > position - variance and word[1] < position + variance):
                    add = False
                    break
            if (add):
                positions.append(word[1])
        return positions

    def wordsSelected(self, variance):
        cols = []
        selected = [[[] for i in range(len(self.centerColumns(variance)))] for j in range(len(self.rows()))]
        for word in self.wordsPosition():           
            intermediate = [] 
            for y, position in enumerate(self.centerColumns(variance)):
                if word[1] > position - variance and word[1] < position + variance:
                    if len(self.selecteda) > 0:
                        for f in self.selecteda:
                            if (y == f):
                                selected[word[2]][y].append(word[0])
                                cols.append(y)
                                break
        result = []
        for d in list(set(cols)):
            result.append(self.column(selected, d))
        return [*zip(*result)]
    
    def column(self, matrix, i):
        return [row[i] for row in matrix]

    def totalColumns(self, variance):
        return len(self.centerColumns(variance))
