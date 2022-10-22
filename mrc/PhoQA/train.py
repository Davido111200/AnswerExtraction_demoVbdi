import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm

from evaluate import evaluate

def train(model, train_dataloader, test_dataloader, optimizer, checkpointer, device, num_epoch):
    #logger = logging.getLogger(__name__)
    #logger.info("***** Running training *****")
    
    for epoch in range(num_epoch):
        model.train()
        for step, batch in enumerate(tqdm(train_dataloader)):
            inputs = {
                'input_ids': batch['input_ids'].to(device),
                'attention_mask': batch['attention_mask'].to(device),
                'token_type_ids': batch['token_type_ids'].to(device),
                'start_positions': batch['start_positions'].to(device),
                'end_positions': batch['end_positions'].to(device),
                'is_impossibles': batch['is_impossibles'].to(device),
                'position_ids': batch['position_ids'].to(device),
            }

            outputs = model(**inputs)
            loss = outputs[0]
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            print('epoch: {}, step: {}, loss: {}'.format(epoch, step, loss.item()))

        checkpointer.save('model_{}'.format(step))
        evaluate(model, test_dataloader, device)