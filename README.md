# DiverSeg dataset (ECCV2024)
This repository provides instructions for downloading datasets and scripts for creating DiverSeg dataset.

Details are described in the following paper:

"Rethinking Image Super-Resolution from Training Data Perspectives",      
Go Ohtani, Ryu Tadokoro, Ryosuke Yamada, Yuki M. Asano, Iro Laina, Christian Rupprecht, Nakamasa Inoue, Rio Yokota, Hirokatsu Kataoka, and Yoshimitsu Aoki, In ECCV2024.
[[arXiv](https://arxiv.org/pdf/2409.00768)]

<div style="text-align: center;">
<img src="fig1.png" alt="ECCV 2024 Logo" width="800"/>
</div>

# Download datasets

## ImageNet (ImageNet-1k)
This dataset can be downloaded from [the official website](https://image-net.org/challenges/LSVRC/2012/2012-downloads.php).
## PASS
You can download this dataset using [this code](https://gist.github.com/yukimasano/421204a5a74a5c150537366a767a1a04).

# Create DiverSeg dataset
Please make sure that the structure of each downloaded dataset is as follows:
```sh
#ImageNet
/path/to/imagenet/
    n01440764/
        n01440764_18.JPEG
        n01440764_36.JPEG
        ...
        ...
    n01443537/
        ...
        ...   
    ...

#PASS
/path/to/pass/
    0/
        0a0bf4db55141fcfff5da2c8655f93.jpg
        0a0c781911dcb7ba44737c02e3b961f.jpg
        ...
        ...
    1/
        ...
        ...   
    ...
```
Run the following scripts to create DiverSeg-I, DiverSeg-P, and DiverSeg-IP datasets.
```sh
#DiverSeg-I
source make_DiverSeg.sh /path/to/imagenet /path/to/DiverSeg-I DiverSeg-I_list.txt

#DiverSeg-P
source make_DiverSeg.sh /path/to/pass /path/to/DiverSeg-P DiverSeg-P_list.txt

#DiverSeg-IP
source make_DiverSeg.sh /path/to/imagenet /path/to/DiverSeg-IP DiverSeg-I_list.txt
source make_DiverSeg.sh /path/to/pass /path/to/DiverSeg-IP DiverSeg-P_list.txt
```

# Citation

If you use our work in your research, please cite our paper:

```bibtex
@InProceedings{ohtani2024rethinking,
    title={Rethinking Image Super-Resolution from Training Data Perspectives},
    author={Ohtani, Go and Tadokoro, Ryu and Yamada, Ryosuke and Asano, Yuki M. and Laina, Iro and Rupprech, Christian and Inoue, Nakamasa and Yokota, Rio and Kataoka, Hirokatsu  and Aoki, Yoshimitsu},
    booktitle={Proceedings of the European Conference on Computer Vision (ECCV)},
    year={2024},
}
```
# Terms of use
All code within the repository follows the MIT License. Each dataset follows the license of the original dataset. The terms of use are as follows:
- DiverSeg-I: non-commercial research and educational purposes
- DiverSeg-P: commercial/research purposes under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)
- DiverSeg-IP: non-commercial research and educational purposes

For more details, please refer to the following links:
- ImageNet [the official website](https://www.image-net.org/download)
- PASS [the official website](https://www.robots.ox.ac.uk/~vgg/data/pass/)

The authors affiliated with National Institute of Advanced Industrial Science and Technology (AIST), Keio University, University of Tsukuba, University of Amsterdam, University of Oxford, and Tokyo Institute of Technology (TITech) are not responsible for the reproduction, duplication, copying, sale, trade, resale, or exploitation of any portion of the data or any derived data for commercial purposes. Additionally, we will not be liable for any damages resulting from the use of this data or any derived data.
