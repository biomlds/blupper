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
