import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def train(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for data in loader:
        data = data.to(device)
        optimizer.zero_grad()
        out = model(data.x, data.edge_index, data.batch)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data.num_graphs
    return total_loss / len(loader.dataset)

def evaluate(model, loader):
    model.eval()
    correct = 0
    y_true = []
    y_pred = []
    for data in loader:
        data = data.to(device)
        out = model(data.x, data.edge_index, data.batch)
        pred = out.argmax(dim=1)
        correct += int((pred == data.y).sum())
        y_true.extend(data.y.cpu().numpy())
        y_pred.extend(pred.cpu().numpy())
    acc = correct / len(loader.dataset)
    return acc, y_true, y_pred