import click
from blupper.mme import mme_solution
from pandas import read_csv

if __name__ == '__main__':

    @click.command()
    @click.option('--input_csv', default='./blupper/tests/test_data/eight_animals_data.csv',
                  help="Table acontaining pedegree and traits information")
    @click.option('--response_var', default='WWG', help='Respomose variable')
    @click.option('--fixed_factor', default=['Sex'], help='Fixed factor in the mixed model')
    @click.option('--sigma_sq_a', default=40, help='Variance(a)')
    @click.option('--sigma_sq_e', default=20, help='Variance(e)')
    @click.option('--output_csv', help='Name of output CSV file')
    def run_mme(input_csv, sigma_sq_a, sigma_sq_e, response_var, fixed_factor, output_csv):
        df = read_csv(input_csv)
        tmp = df.Dam[df.Dam != 'Unknown'].map(int)
        df.Dam = [int(i) if i != 'Unknown' else i for i in df.Dam]
        df_out = mme_solution(df, sigma_sq_a, sigma_sq_e,
                              response_var, fixed_factor)
        df_out.to_csv(output_csv, index=None)
    run_mme()
