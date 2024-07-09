# DiverSeg dataset (ECCV2024)
This repository provides instructions for downloading datasets and scripts for creating DiverSeg dataset.

Details are described in the following paper:

"Rethinking Image Super-Resolution from Training Data Perspectives",      
Go Ohtani, Ryu Tadokoro, Ryosuke Yamada, Yuki M. Asano, Iro Laina, Christian Rupprecht, Nakamasa Inoue, Rio Yokota, Hirokatsu Kataoka, and Yoshimitsu Aoki, In ECCV2024.

<div style="text-align: center;">
<img src="fig1.png" alt="ECCV 2024 Logo" width="800"/>
</div>

# Download datasets
Please download datasets. For ImageNet, it needs to be downloaded from the official website.

## ImageNet (ILSVRC2012)
This dataset can be downloaded from [the official website]((https://www.image-net.org/download.php)).
## PASS
Please see [zenodo](https://zenodo.org/records/6615455) for the raw dataset. Alternatively, execute the following commands:
```sh
git clone https://github.com/yukimasano/PASS
cd PASS
```
Note: Before running download.sh, replace line 8 with:
```sh
curl https://zenodo.org/records/6615455/files/PASS.${PART}.tar --output PASS.${PART}.tar
```
Then run:
```sh
source download.sh # maybe change the directory where you want to download it
```

# Create DiverSeg dataset
Run the following scripts to create DiverSeg-I, DiverSeg-P, and DiverSeg-IP datasets.
```sh
#DiverSeg-I
source make_DiverSeg.sh path/to/ImageNet-1k path/to/DiverSeg-I DiverSeg-I_list.txt

#DiverSeg-P
source make_DiverSeg.sh path/to/PASS path/to/DiverSeg-P DiverSeg-P_list.txt

#DiverSeg-IP
source make_DiverSeg.sh path/to/ImageNet-1k path/to/DiverSeg-IP DiverSeg-I_list.txt
source make_DiverSeg.sh path/to/PASS path/to/DiverSeg-IP DiverSeg-P_list.txt
```

