
import matplotlib.pyplot as plt

from PIL import Image

img1 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/Heatmap25rExpertNoAveByAcc04172023/MetaAnalysisExpertNoExpert/Group1_11tobii_overlay_short.png'
img2 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/EfficientNetOccSegment/overlay-k20-thresh0.05-pixcut20-KSSlide133v2_heatmappositiveAverage.png'
img3 = 'C:/Users/duongdb/Documents/Face11CondTobiiEyeTrack01112023/EfficientNetOccSegment/overlay-k20-thresh0.05-pixcut70-KSSlide133v2_heatmappositiveAverage.png'


img1 = Image.open(img1)

img2 = Image.open(img2)

img3 = Image.open(img3)


fig, (ax_1, ax_2, ax_3) = plt.subplots(nrows=1, ncols=3, figsize=(11,8), gridspec_kw={'width_ratios': [3, 1, 1]})

ax_1.set_title('Participant visual heat maps')
ax_1.imshow(img1)
ax_1.xaxis.set_visible(False)
ax_1.yaxis.set_visible(False)

ax_2.set_title('Saliency map')
ax_2.imshow(img2)
ax_2.xaxis.set_visible(False)
ax_2.yaxis.set_visible(False)

# ax_3.set_title('C')
ax_3.imshow(img3)
ax_3.xaxis.set_visible(False)
ax_3.yaxis.set_visible(False)

# fig.suptitle('Name')
plt.show()


fig = plt.figure(figsize=(5.5, 3.5))
spec = fig.add_gridspec(2, 3)
ax0 = fig.add_subplot(spec[:, 0])
ax0.imshow(img1)

ax1 = fig.add_subplot(spec[0, 1])
ax1.imshow(img2)

ax2 = fig.add_subplot(spec[0, 2])
ax2.imshow(img3)
plt.show()


