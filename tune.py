import sys


# Tune parameters using Twiddle algorithm

# Args:
#  params: Dictionary of parameters with initial values;
#  cost_function: Function that takes a dictionary of parameters and returns an error or a fitting value;
#  d_params: Optional dictionary of step sizes in each parameter direction (if not specified: default value = 1);
#  threshold: Stop iteration if error does not improve by at least this value

def tune_twiddle(params, cost_function, d_params=None, threshold=0.001):
    if d_params is None:
        d_params = dict((key, 1.) for (key, _) in params.items())

    prev_err = sys.float_info.max
    err = sys.float_info.max / 2

    while (prev_err - err) > threshold:
        prev_err = err

        for k in params.keys():
            params[k] += d_params[k]
            e = cost_function(params)

            if e < err:
                err = e
                d_params[k] *= 1.1
            else:
                params[k] -= 2 * d_params[k]
                e = cost_function(params)

                if e < err:
                    err = e
                    d_params[k] *= 1.1
                else:
                    params[k] += d_params[k]
                    d_params[k] *= 0.95

    return params
