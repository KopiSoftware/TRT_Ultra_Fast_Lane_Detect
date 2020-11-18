from __future__ import print_function

import os
import argparse

import tensorrt as trt

#from plugins import add_yolo_plugins


EXPLICIT_BATCH = []
if trt.__version__[0] >= '7':
    EXPLICIT_BATCH.append(
        1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))


def build_engine(onnx_file_path, verbose=False):
    """Build a TensorRT engine from an ONNX file."""
    TRT_LOGGER = trt.Logger(trt.Logger.VERBOSE) if verbose else trt.Logger()
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network(*EXPLICIT_BATCH) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
        builder.max_workspace_size = 1 << 28
        builder.max_batch_size = 1
        builder.fp16_mode = False
        #builder.strict_type_constraints = True

        # Parse model file
        print('Loading ONNX file from path {}...'.format(onnx_file_path))
        with open(onnx_file_path, 'rb') as model:
            if not parser.parse(model.read()):
                print('ERROR: Failed to parse the ONNX file.')
                for error in range(parser.num_errors):
                    print(parser.get_error(error))
                return None
        #if trt.__version__[0] >= '7':
            # The actual yolo*.onnx is generated with batch size 64.
            # Reshape input to batch size 1
        #    shape = list(network.get_input(0).shape)
        #    shape[0] = 1
        #    network.get_input(0).shape = shape

        print('Adding yolo_layer plugins...')
        model_name = onnx_file_path[:-5]
        #network = add_yolo_plugins(
        #    network, model_name, category_num, TRT_LOGGER)

        print('Building an engine.  This would take a while...')
        print('(Use "--verbose" to enable verbose logging.)')
        engine = builder.build_cuda_engine(network)
        print('Completed creating engine.')
        return engine


def main():
    """Create a TensorRT engine for ONNX-based YOLO."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='enable verbose output (for debugging)')
    parser.add_argument(
        '-c', '--category_num', type=int, default=4,
        help='number of object categories [80]')
    parser.add_argument(
        '-m', '--model', type=str, default='model',     # 修改这里即可,例如：res18_lane.pth->default='res18_lane'
        help=('[yolov3|yolov3-tiny|yolov3-spp|yolov4|yolov4-tiny]-'
              '[{dimension}], where dimension could be a single '
              'number (e.g. 288, 416, 608) or WxH (e.g. 416x256)'))
    args = parser.parse_args() 

    onnx_file_path = '%s.onnx' % args.model
    if not os.path.isfile(onnx_file_path):
        raise SystemExit('ERROR: file (%s) not found!  You might want to run yolo_to_onnx.py first to generate it.' % onnx_file_path)
    engine_file_path = '%s.trt' % args.model
    engine = build_engine(onnx_file_path, args.verbose)
    with open(engine_file_path, 'wb') as f:
        f.write(engine.serialize())
    print('Serialized the TensorRT engine to file: %s' % engine_file_path)


if __name__ == '__main__':
    main()
