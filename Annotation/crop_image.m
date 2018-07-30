%% Load the image

im = imread('C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0.ome.tif_Filtered-Max.tif');


%% Crop
x_i = 1100;
y_i = 400;
height = 450;
max_width = 700;

im_rescale = imcrop(im, [x_i y_i max_width height]);

max_intensity = max(max(im_rescale));

% Rescale so the max is at 80%
im_rescale = im2uint8(im_rescale * ((2^16 - 1) / (max_intensity / 0.8)));


for width = 300:200:max_width
   
    file_name = sprintf('C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_%s.png', int2str(width));
    
    im_crop = imcrop(im_rescale, [0 0 width height]);
    
    imwrite(im_crop, file_name)

    
    file_name = sprintf('C2-ISP_293T_TFRC_InSituPrep_20180712_1_MMStack_Pos0_%s_inv.png', int2str(width));
    
    imwrite(imcomplement(im_crop), file_name);
    
end