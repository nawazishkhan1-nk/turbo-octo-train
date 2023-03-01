#! /usr/bin/env python

""" Top-level script for generating data (in the data sets where that is necessary) """

import argparse
import sys
import numpy as np
import logging

sys.path.append("../../../")

from experiments.datasets import load_simulator
from experiments.utils import create_filename

logger = logging.getLogger(__name__)


def parse_args():
    """ Parses command-line arguments for data generation """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        type=str,
        default="spherical_gaussian",
        choices=["power", "spherical_gaussian", "conditional_spherical_gaussian", "lorenz"],
        help="Dataset: spherical_gaussian, power, and conditional_spherical_gaussian",
    )
    parser.add_argument("-i", type=int, default=0, help="Run number")

    parser.add_argument("--truelatentdim", type=int, default=2, help="True manifold dimensionality (for datasets where that is variable)")
    parser.add_argument("--datadim", type=int, default=3, help="True data dimensionality (for datasets where that is variable)")
    parser.add_argument("--epsilon", type=float, default=0.01, help="Noise term (for datasets where that is variable)")
    parser.add_argument("--train", type=int, default=1000000, help="Number of training samples")
    parser.add_argument("--paramscan", type=int, default=0, help="Number of additional test samples for parameter tuning")
    parser.add_argument("--test", type=int, default=10000, help="Number of test samples")
    parser.add_argument("--ood", type=int, default=0, help="Number of OOD samples")

    parser.add_argument("--dir", type=str, default="/scratch/jb6504/manifold-flow", help="Base directory of repo")
    parser.add_argument("--debug", action="store_true", help="Debug mode (more log output, additional callbacks)")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logging.basicConfig(format="%(asctime)-5.5s %(name)-20.20s %(levelname)-7.7s %(message)s", datefmt="%H:%M", level=logging.DEBUG if args.debug else logging.INFO)
    logger.info("Hi!")
    logger.debug("Starting generate_data.py with arguments %s", args)

    # Simulator
    simulator = load_simulator(args)

    # Parameters?
    conditional = simulator.parameter_dim() is not None

    parameters_train = simulator.sample_from_prior(args.train) if conditional else None

    # Sample
    if args.train > 0:
        logger.info("Generating %s training samples at parameters %s", args.train, parameters_train)
        x_train = simulator.sample(args.train, parameters=parameters_train)
        np.save(create_filename("sample", "x_train", args), x_train)
        if conditional:
            np.save(create_filename("sample", "theta_train", args), parameters_train)

    if args.paramscan > 0:
        parameters_val = np.array([simulator.default_parameters() for _ in range(args.paramscan)]).reshape((args.paramscan, -1)) if conditional else None
        logger.info("Generating %s param-scan samples at parameters %s", args.paramscan, parameters_val)
        x_val = simulator.sample(args.paramscan, parameters=parameters_val)
        np.save(create_filename("sample", "x_paramscan", args), x_val)
        if conditional:
            np.save(create_filename("sample", "theta_paramscan", args), parameters_val)

    if args.test > 0:
        parameters_test = np.array([simulator.default_parameters() for _ in range(args.test)]).reshape((args.test, -1)) if conditional else None
        logger.info("Generating %s test samples at parameters %s", args.test, parameters_test)
        x_test = simulator.sample(args.test, parameters=parameters_test)
        np.save(create_filename("sample", "x_test", args), x_test)
        if conditional:
            np.save(create_filename("sample", "theta_test", args), parameters_test)

    if args.ood > 0:
        logger.info("Generating %s ood samples at parameters %s", args.ood, parameters_test)
        x_ood = simulator.sample_ood(args.ood, parameters=parameters_test)
        np.save(create_filename("sample", "x_ood", args), x_ood)
        if conditional:
            np.save(create_filename("sample", "theta_ood", args), parameters_test)

    logger.info("All done! Have a nice day!")
