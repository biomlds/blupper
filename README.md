# blupper

Mixed linear model for the prediction of breeding values and estimation of fixed effects under an animal model. The model is implemented and tested on data from Chapter 3 (Mrode RA, 2014).


Consider the data set in Table 3.1 for the pre-weaning gain (WWG) of beef calves (calves assumed to be reared under the same management conditions).

<img src="https://render.githubusercontent.com/render/math?math=y_{ij} =p_{ij} %2B a_{j} %2B e_{ij}">

where: Yij = the WWG of the jth calf of the ith sex; Pi = the fixed effect of the ith sex; Aj = random effect of the jth calf; and eij = random error effect.



----
Example 3.1.

| Calf | Sire | Dam     | Sex    | WWG (Kg) |
| ---- | :--- | :------ | :----- | :------- |
| 4    | 1    | Unknown | Male   | 4.51     |
| 5    | 3    | 2       | Female | 2.92     |
| 6    | 1    | 2       | Female | 3.93     |
| 7    | 4    | 5       | Male   | 3.54     |
| 8    | 3    | 6       | Male   | 5.0      |


## Test the package on the Example 3.1

```
python setup.py test
```

## Installation
```
pip install -e  blupper
```

## Usage

Following command
```
python blup_generator.py  --input_csv  ./blupper/tests/test_data/eight_animals_data.csv --output_csv OUT.csv --sigma_sq_a 20 --sigma_sq_e 40 --response_var WWG
```

Produce this table:

| Animal | BLUP                  | r_squared            | r                   | SEP               |
| :----: | :-------------------- | :------------------- | :------------------ | :---------------- |
|   1    | 0.09844457570387988   | 0.057811577082102494 | 0.2404403815545602  | 4.34094096462483  |
|   2    | -0.018770099100871906 | 0.01580855811511439  | 0.12573208864531915 | 4.436646124912118 |
|   3    | -0.04108420292708481  | 0.08708243092472268  | 0.29509732449604265 | 4.272979216133113 |
|   4    | -0.008663122661940692 | 0.14463969285292366  | 0.3803152545624796  | 4.136085848110691 |
|   5    | -0.1857320994946512   | 0.14378650653015657  | 0.37919191253263373 | 4.138148120765721 |
|   6    | 0.17687208768130214   | 0.11543446872743957  | 0.3397564844523789  | 4.206103972258794 |
|   7    | -0.24945855483363033  | 0.11628765505020666  | 0.3410097579985163  | 4.20407503489125  |
|   8    | 0.18261468793069424   | 0.15527170702894255  | 0.3940453108830792  | 4.110299971951092 |