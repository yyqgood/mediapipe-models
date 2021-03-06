import tensorflow as tf
import numpy as np
import tensorflow.keras.backend as K

def get_pretrained_tflite_weights(model_path):
    model = tf.lite.Interpreter(model_path)
    tensor_details = model.get_tensor_details()
    weights_dict = {}
    layer_names = []
    
    for idx in range(0, len(tensor_details)):
        try:
            name = tensor_details[idx]['name']
            weights = model.get_tensor(idx)
            weights_dict[name] = weights
        except:
            name = tensor_details[idx]['name']
            layer_names.append(name)
    return weights_dict, layer_names

def set_pretrained_weights(model, weights_dict, layer_names):
    for name in layer_names:
        if name.find('conv') != -1:
            pretrained_weights = []
            kernel_weight = weights_dict.get(name+'/Kernel')
            bias_weight = weights_dict.get(name+'/Bias')
            kernel_weight = kernel_weight.transpose(1, 2, 3, 0)
            pretrained_weights.append(kernel_weight)
            pretrained_weights.append(bias_weight)
            layer = model.get_layer(name)
            layer.set_weights(pretrained_weights)
        
        elif name.find('p_re_lu') != -1:
            pretrained_weights = []
            alpha_weight = weights_dict.get(name+'/Alpha')
            pretrained_weights.append(alpha_weight)
            
            layer = model.get_layer(name)
            layer.set_weights(pretrained_weights)

def display_nodes(nodes):
    for i, node in enumerate(nodes):
        print('%d %s %s' % (i, node.name, node.op))
        for idx, n in enumerate(node.input):
            print(u'└─── %d ─ %s' % (idx, n))
