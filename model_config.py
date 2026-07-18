# model_config.py

# The exact 222 features your model expects in order
FEATURE_NAMES = [
    "MSSubClass","LotFrontage","LotArea","OverallQual","OverallCond","YearBuilt","YearRemodAdd",
    "MasVnrArea","ExterQual","ExterCond","BsmtQual","BsmtCond","BsmtFinSF1","BsmtFinSF2",
    "BsmtUnfSF","TotalBsmtSF","HeatingQC","1stFlrSF","2ndFlrSF","LowQualFinSF","GrLivArea",
    "BsmtFullBath","BsmtHalfBath","FullBath","HalfBath","BedroomAbvGr","KitchenAbvGr",
    "KitchenQual","TotRmsAbvGrd","Fireplaces","FireplaceQu","GarageYrBlt","GarageCars",
    "GarageArea","GarageQual","GarageCond","WoodDeckSF","OpenPorchSF","EnclosedPorch",
    "3SsnPorch","ScreenPorch","PoolArea","MiscVal","MoSold","YrSold","HouseAge","RemodelAge",
    "TotalBathrooms","TotalLivingArea","TotalPorchArea","HasGarage","HasBasement","HasFireplace",
    "HasPool","MSZoning_FV","MSZoning_RH","MSZoning_RL","MSZoning_RM","Alley_None","Alley_Pave",
    "LotShape_IR2","LotShape_IR3","LotShape_Reg","LandContour_HLS","LandContour_Low",
    "LandContour_Lvl","LotConfig_CulDSac","LotConfig_FR2","LotConfig_FR3","LotConfig_Inside",
    "LandSlope_Mod","LandSlope_Sev","Neighborhood_Blueste","Neighborhood_BrDale",
    "Neighborhood_BrkSide","Neighborhood_ClearCr","Neighborhood_CollgCr","Neighborhood_Crawfor",
    "Neighborhood_Edwards","Neighborhood_Gilbert","Neighborhood_IDOTRR","Neighborhood_MeadowV",
    "Neighborhood_Mitchel","Neighborhood_NAmes","Neighborhood_NPkVill","Neighborhood_NWAmes",
    "Neighborhood_NoRidge","Neighborhood_NridgHt","Neighborhood_OldTown","Neighborhood_SWISU",
    "Neighborhood_Sawyer","Neighborhood_SawyerW","Neighborhood_Somerst","Neighborhood_StoneBr",
    "Neighborhood_Timber","Neighborhood_Veenker","Condition1_Feedr","Condition1_Norm",
    "Condition1_PosA","Condition1_PosN","Condition1_RRAe","Condition1_RRAn","Condition1_RRNe",
    "Condition1_RRNn","BldgType_2fmCon","BldgType_Duplex","BldgType_Twnhs","BldgType_TwnhsE",
    "HouseStyle_1.5Unf","HouseStyle_1Story","HouseStyle_2.5Fin","HouseStyle_2.5Unf",
    "HouseStyle_2Story","HouseStyle_SFoyer","HouseStyle_SLvl","RoofStyle_Gable",
    "RoofStyle_Gambrel","RoofStyle_Hip","RoofStyle_Mansard","RoofStyle_Shed","RoofMatl_CompShg",
    "RoofMatl_Metal","RoofMatl_Roll","RoofMatl_Tar&Grv","RoofMatl_WdShake","RoofMatl_WdShngl",
    "Exterior1st_AsphShn","Exterior1st_BrkComm","Exterior1st_BrkFace","Exterior1st_CBlock",
    "Exterior1st_CemntBd","Exterior1st_HdBoard","Exterior1st_ImStucc","Exterior1st_MetalSd",
    "Exterior1st_Plywood","Exterior1st_Stone","Exterior1st_Stucco","Exterior1st_VinylSd",
    "Exterior1st_Wd Sdng","Exterior1st_WdShing","Exterior2nd_AsphShn","Exterior2nd_Brk Cmn",
    "Exterior2nd_BrkFace","Exterior2nd_CBlock","Exterior2nd_CmentBd","Exterior2nd_HdBoard",
    "Exterior2nd_ImStucc","Exterior2nd_MetalSd","Exterior2nd_Other","Exterior2nd_Plywood",
    "Exterior2nd_Stone","Exterior2nd_Stucco","Exterior2nd_VinylSd","Exterior2nd_Wd Sdng",
    "Exterior2nd_Wd Shng","MasVnrType_BrkFace","MasVnrType_None","MasVnrType_Stone",
    "Foundation_CBlock","Foundation_PConc","Foundation_Slab","Foundation_Stone","Foundation_Wood",
    "BsmtExposure_Gd","BsmtExposure_Mn","BsmtExposure_No","BsmtExposure_None","BsmtFinType1_BLQ",
    "BsmtFinType1_GLQ","BsmtFinType1_LwQ","BsmtFinType1_None","BsmtFinType1_Rec","BsmtFinType1_Unf",
    "BsmtFinType2_BLQ","BsmtFinType2_GLQ","BsmtFinType2_LwQ","BsmtFinType2_None","BsmtFinType2_Rec",
    "BsmtFinType2_Unf","Heating_GasA","Heating_GasW","Heating_Grav","Heating_OthW","Heating_Wall",
    "CentralAir_Y","Electrical_FuseF","Electrical_FuseP","Electrical_SBrkr","Functional_Maj2",
    "Functional_Min1","Functional_Min2","Functional_Mod","Functional_Sev","Functional_Typ",
    "GarageType_Attchd","GarageType_Basment","GarageType_BuiltIn","GarageType_CarPort",
    "GarageType_Detchd","GarageType_None","GarageFinish_None","GarageFinish_RFn",
    "GarageFinish_Unf","PavedDrive_P","PavedDrive_Y","Fence_GdWo","Fence_MnPrv","Fence_MnWw",
    "Fence_None","SaleType_CWD","SaleType_Con","SaleType_ConLD","SaleType_ConLI","SaleType_ConLw",
    "SaleType_New","SaleType_Oth","SaleType_WD","SaleCondition_AdjLand","SaleCondition_Alloca",
    "SaleCondition_Family","SaleCondition_Normal","SaleCondition_Partial"
]

# Categorical mapping lists to populate selectboxes for the user
NEIGHBORHOODS = ["Blueste", "BrDale", "BrkSide", "ClearCr", "CollgCr", "Crawfor", "Edwards", "Gilbert", "IDOTRR", "MeadowV", "Mitchel", "NAmes", "NPkVill", "NWAmes", "NoRidge", "NridgHt", "OldTown", "SWISU", "Sawyer", "SawyerW", "Somerst", "StoneBr", "Timber", "Veenker"]
MS_ZONING = ["FV", "RH", "RL", "RM"]
HOUSE_STYLE = ["1.5Unf", "1Story", "2.5Fin", "2.5Unf", "2Story", "SFoyer", "SLvl"]
GARAGE_TYPE = ["Attchd", "Basment", "BuiltIn", "CarPort", "Detchd", "None"]