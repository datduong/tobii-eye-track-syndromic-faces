## Compare human and computer visual attention in assessing genetic conditions

Final paper will be available very soon [(first draft)](https://www.medrxiv.org/content/10.1101/2023.07.26.23293119v1). 

All images were collected via online search; however, due to redistribution copyright issues, we cannot freely redistribute these images. Please contact us for the dataset.

Our main objective is to observe how clinicians and nonclinicians inspect pictures of syndromic faces. Tobii eye tracking device was used to collect visual attention heat maps of the clinicians and nonclinicians. Next, we used [intersection-over-union](https://www.nature.com/articles/s42256-022-00536-x) and Kullback–Leibler (KL) divergence to compare the visual heat maps. 

For example, this the [last image on this page here](https://www.funtoday.news/post02236391146685) shows an individual affected with Kabuki Syndrome. The key features are the outter corner of the eyes. This was one of the images tested in our paper. The example output below shows the visual attention heat maps of clinicians (top row) vs nonclinicians (bottom row). The overall visual attivity looks simlar for both clinicians and nonclinicians (left most column). However, when narrowing down to areas with the highest visual attivity (e.g. where people spend the most of time looking at), then we observe drastic differences between clinicians and nonclinicians.  

<br />

* The average visual attentions of clinicians and nonclinicians on an example image of Kabuki Syndrome at different intensities. 

<div>
    <img src="https://github.com/datduong/tobii-eye-track-syndromic-faces/blob/master/example_img/Kabuki_clinicians_vs_nonclinicians.png" width="100%">
</div>

<br />
<br />
<br />


We further compared how saliency maps of a deep learning classifier against human visual heat map. Our classifier is at [this other repo](https://github.com/datduong/classify-syndromic-faces). Our classifier is not state-of-the-art; the goal is to observe preliminary differences between human vs. machine. 

Please see [`experiment`](https://github.com/datduong/tobii-eye-track-syndromic-faces/tree/master/experiment) for more instructions on running this repo. 



